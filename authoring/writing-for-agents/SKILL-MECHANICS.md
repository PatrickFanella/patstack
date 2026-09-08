# Codex skill mechanics

Names, descriptions, and paths support discovery; bodies and resources load when needed. Use concise automatic entrypoints for distinct jobs and conditional references for related procedures. Explicit-only invocation uses `policy.allow_implicit_invocation: false` in `agents/openai.yaml`; preserve the user’s chosen invocation behavior. A reference file can be read directly without invoking another skill. Do not use legacy `disable-model-invocation` as a Codex policy.
