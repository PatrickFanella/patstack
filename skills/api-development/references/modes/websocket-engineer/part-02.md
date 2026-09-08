## Core Workflow

1. **Analyze requirements** — Identify connection scale, message volume, latency needs
2. **Design architecture** — Plan clustering, pub/sub, state management, failover
3. **Implement** — Build WebSocket server with authentication, rooms, events
4. **Validate locally** — Test connection handling, auth, and room behavior before scaling (e.g., `npx wscat -c ws://localhost:3000`); confirm auth rejection on missing/invalid tokens, room join/leave events, and message delivery
5. **Scale** — Verify Redis connection and pub/sub round-trip before enabling the adapter; configure sticky sessions and confirm with test connections across multiple instances; set up load balancing
6. **Monitor** — Track connections, latency, throughput, error rates; add alerts for connection-count spikes and error-rate thresholds
