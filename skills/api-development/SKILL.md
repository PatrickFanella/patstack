---
name: api-development
description: 'API contracts and backend protocols: REST/GraphQL, OpenAPI, Node services, and WebSocket lifecycle design.'
---

# api-development

Start with the public contract and the existing framework. Keep transport validation, authentication, business rules, and persistence responsibilities explicit. Load WebSocket guidance only for long-lived connections.

## Select a mode

- Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers. Read [the procedure](references/modes/api-design-principles/guide.md).
- Build production-ready Node.js backend services with Express/Fastify, implementing middleware patterns, error handling, authentication, database integration, and API design best practices. Read [the procedure](references/modes/nodejs-backend-patterns/guide.md).
- Generate and maintain OpenAPI 3.1 specifications from code, design-first specs, and validation patterns. Read [the procedure](references/modes/openapi-spec-generation/guide.md).
- Use when building real-time communication systems with WebSockets or Socket.IO. Read [the procedure](references/modes/websocket-engineer/guide.md).

Resource paths inside a mode are relative to that mode directory. Run its scripts from that directory or use absolute script paths, passing the target repository explicitly.
