#!/usr/bin/env python3
"""Deterministic, read-only MCP stdio initialize/catalog probe."""

from __future__ import annotations

import argparse
import json
import os
import selectors
import subprocess
import sys
import threading
import time
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Launch an MCP stdio server, initialize it, list tools/resources, "
            "and terminate only the spawned child."
        )
    )
    parser.add_argument("--cwd", help="Working directory for the server")
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Environment override; repeat as needed (values are never printed)",
    )
    parser.add_argument(
        "--protocol-version", default="2024-11-05", help="Requested MCP version"
    )
    parser.add_argument(
        "--timeout", type=float, default=10.0, help="Seconds per response"
    )
    parser.add_argument("--expect-tool", action="append", default=[])
    parser.add_argument("--expect-resource", action="append", default=[])
    parser.add_argument("--expect-prompt", action="append", default=[])
    parser.add_argument(
        "--show-stderr",
        action="store_true",
        help="Print captured server stderr on failure; may contain sensitive data",
    )
    parser.add_argument(
        "command", nargs=argparse.REMAINDER, help="Server command after --"
    )
    args = parser.parse_args()
    if args.command[:1] == ["--"]:
        args.command = args.command[1:]
    if not args.command:
        parser.error("a server command is required after --")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    return args


def build_env(overrides: list[str]) -> dict[str, str]:
    result = os.environ.copy()
    for item in overrides:
        key, separator, value = item.partition("=")
        if not separator or not key or "\x00" in item:
            raise ValueError(f"invalid --env entry: {key or '<empty>'}")
        result[key] = value
    return result


class Protocol:
    def __init__(self, process: subprocess.Popen[bytes], timeout: float) -> None:
        assert process.stdin is not None
        assert process.stdout is not None
        self.process = process
        self.timeout = timeout
        self.selector = selectors.DefaultSelector()
        self.selector.register(process.stdout, selectors.EVENT_READ)
        self.buffer = b""

    def send(self, message: dict[str, Any]) -> None:
        payload = json.dumps(message, separators=(",", ":"), sort_keys=True)
        assert self.process.stdin is not None
        self.process.stdin.write(payload.encode("utf-8") + b"\n")
        self.process.stdin.flush()

    def read_message(self, deadline: float) -> dict[str, Any]:
        while True:
            line, separator, rest = self.buffer.partition(b"\n")
            if separator:
                self.buffer = rest
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except (UnicodeDecodeError, json.JSONDecodeError) as error:
                    preview = line[:160].decode("utf-8", errors="replace")
                    raise RuntimeError(f"non-JSON stdout: {preview!r}") from error
                if not isinstance(value, dict):
                    raise RuntimeError("stdout JSON message is not an object")
                return value

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"response timed out after {self.timeout:g}s")
            if not self.selector.select(remaining):
                raise TimeoutError(f"response timed out after {self.timeout:g}s")
            assert self.process.stdout is not None
            chunk = os.read(self.process.stdout.fileno(), 65536)
            if not chunk:
                raise RuntimeError("server closed stdout before responding")
            self.buffer += chunk

    def request(
        self, request_id: int, method: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        message: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
        }
        if params is not None:
            message["params"] = params
        self.send(message)
        deadline = time.monotonic() + self.timeout
        while True:
            response = self.read_message(deadline)
            if response.get("id") != request_id:
                continue
            if response.get("jsonrpc") != "2.0":
                raise RuntimeError(f"{method}: invalid JSON-RPC version")
            if "error" in response:
                error = response["error"]
                raise RuntimeError(f"{method}: JSON-RPC error {error!r}")
            result = response.get("result")
            if not isinstance(result, dict):
                raise RuntimeError(f"{method}: missing object result")
            return result


def string_fields(items: Any, field: str) -> list[str]:
    if not isinstance(items, list):
        raise RuntimeError("catalog result is not a list")
    values: list[str] = []
    for item in items:
        if isinstance(item, dict) and isinstance(item.get(field), str):
            values.append(item[field])
    return sorted(values)


def drain(stream: Any, sink: bytearray) -> None:
    while True:
        chunk = stream.read(65536)
        if not chunk:
            return
        sink.extend(chunk)
        if len(sink) > 65536:
            del sink[:-65536]


def stop_child(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=2)


def main() -> int:
    args = parse_args()
    stderr = bytearray()
    process: subprocess.Popen[bytes] | None = None
    try:
        process = subprocess.Popen(
            args.command,
            cwd=args.cwd,
            env=build_env(args.env),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
        assert process.stderr is not None
        stderr_thread = threading.Thread(
            target=drain, args=(process.stderr, stderr), daemon=True
        )
        stderr_thread.start()
        protocol = Protocol(process, args.timeout)
        initialized = protocol.request(
            1,
            "initialize",
            {
                "protocolVersion": args.protocol_version,
                "capabilities": {},
                "clientInfo": {
                    "name": "mcp-integration-lifecycle-probe",
                    "version": "1.0.0",
                },
            },
        )
        negotiated = initialized.get("protocolVersion")
        if not isinstance(negotiated, str):
            raise RuntimeError("initialize: missing protocolVersion")
        capabilities = initialized.get("capabilities")
        if not isinstance(capabilities, dict):
            raise RuntimeError("initialize: missing capabilities")
        protocol.send(
            {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {},
            }
        )
        next_id = 2
        tools_supported = isinstance(capabilities.get("tools"), dict)
        resources_supported = isinstance(capabilities.get("resources"), dict)
        prompts_supported = isinstance(capabilities.get("prompts"), dict)
        tools: list[str] = []
        resources: list[str] = []
        prompts: list[str] = []
        if tools_supported:
            tools = string_fields(
                protocol.request(next_id, "tools/list").get("tools"), "name"
            )
            next_id += 1
        if resources_supported:
            resources = string_fields(
                protocol.request(next_id, "resources/list").get("resources"), "uri"
            )
            next_id += 1
        if prompts_supported:
            prompts = string_fields(
                protocol.request(next_id, "prompts/list").get("prompts"), "name"
            )
        missing_tools = sorted(set(args.expect_tool) - set(tools))
        missing_resources = sorted(set(args.expect_resource) - set(resources))
        missing_prompts = sorted(set(args.expect_prompt) - set(prompts))
        summary = {
            "missing_prompts": missing_prompts,
            "missing_resources": missing_resources,
            "missing_tools": missing_tools,
            "prompt_count": len(prompts),
            "prompts": prompts,
            "prompts_supported": prompts_supported,
            "protocol_version": negotiated,
            "resource_count": len(resources),
            "resources": resources,
            "resources_supported": resources_supported,
            "status": (
                "ok"
                if not missing_tools and not missing_resources and not missing_prompts
                else "drift"
            ),
            "tool_count": len(tools),
            "tools": tools,
            "tools_supported": tools_supported,
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0 if summary["status"] == "ok" else 1
    except (OSError, ValueError, RuntimeError, TimeoutError) as error:
        print(f"probe failed: {error}", file=sys.stderr)
        if args.show_stderr and stderr:
            print("--- server stderr (tail) ---", file=sys.stderr)
            print(stderr.decode("utf-8", errors="replace"), file=sys.stderr)
        return 2
    finally:
        if process is not None:
            stop_child(process)


if __name__ == "__main__":
    raise SystemExit(main())
