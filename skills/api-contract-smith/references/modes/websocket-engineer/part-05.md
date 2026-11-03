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
