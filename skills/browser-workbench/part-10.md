## Maintaining this skill

- Keep activation low-noise: only use this skill for isolated GUI/browser work.
- Keep context small: frontmatter loads by default; body loads on activation;
  tool schemas load on demand.
- Omit `allowed-tools` intentionally: different hosts namespace MCP tools
  differently, and the skill routes the full family progressively.
- Validate with `agnix --target generic|claude-code|cursor|codex|kiro`
  when changing this file.
