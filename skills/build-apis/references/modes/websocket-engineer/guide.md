# WebSocket engineer

Paths here are relative to this mode directory; pass the target repository explicitly.

## Core Workflow

1. **Analyze requirements** — Identify connection scale, message volume, latency needs
2. **Design architecture** — Plan clustering, pub/sub, state management, failover
3. **Implement** — Build WebSocket server with authentication, rooms, events
4. **Validate locally** — Test connection handling, auth, and room behavior before scaling (e.g., `npx wscat -c ws://localhost:3000`); confirm auth rejection on missing/invalid tokens, room join/leave events, and message delivery
5. **Scale** — Verify Redis connection and pub/sub round-trip before enabling the adapter; configure sticky sessions and confirm with test connections across multiple instances; set up load balancing
6. **Monitor** — Track connections, latency, throughput, error rates; add alerts for connection-count spikes and error-rate thresholds

## Constraints

### MUST DO
- Use sticky sessions for load balancing (WebSocket connections are stateful — requests must route to the same server instance)
- Implement heartbeat/ping-pong to detect dead connections (TCP keepalive alone is insufficient)
- Use rooms/namespaces for message scoping rather than filtering in application logic
- Queue messages during disconnection windows to avoid silent data loss
- Plan connection limits per instance before scaling horizontally

### MUST NOT DO
- Store large state in memory without a clustering strategy (use Redis or an external store)
- Mix WebSocket and HTTP on the same port without explicit upgrade handling
- Forget to handle connection cleanup (presence records, room membership, in-flight timers)
- Skip load testing before production — connection-count spikes behave differently from HTTP traffic spikes

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Protocol | `references/protocol.md` | WebSocket handshake, frames, ping/pong, close codes |
| Scaling | `references/scaling.md` | Horizontal scaling, Redis pub/sub, sticky sessions |
| Patterns | `references/patterns.md` | Rooms, namespaces, broadcasting, acknowledgments |
| Security | `references/security.md` | Authentication, authorization, rate limiting, CORS |
| Alternatives | `references/alternatives.md` | SSE, long polling, when to choose WebSockets |

## Output Templates

When implementing WebSocket features, provide:
1. Server setup (Socket.IO/ws configuration)
2. Event handlers (connection, message, disconnect)
3. Client library (connection, events, reconnection)
4. Brief explanation of scaling strategy

## Read when needed

- [Code examples](part-04.md): read when writing a Socket.IO server with auth, rooms and the Redis adapter, or a reconnecting client with a send queue.
