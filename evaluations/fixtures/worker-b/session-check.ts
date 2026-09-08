import { fixture, reconcile } from "./session.ts";

const cancelled = reconcile(fixture, false);
if (cancelled.status !== "cancelled") throw new Error("missing worker must cancel running session");

const afterStaleEvent = reconcile(cancelled, true);
if (afterStaleEvent.status !== "cancelled") throw new Error("terminal state must not regress");

console.log(`lifecycle ok: ${fixture.status} -> ${cancelled.status} -> ${afterStaleEvent.status}`);
