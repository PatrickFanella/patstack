## Defaults And Decision Rules

- Treat the root `README.md` as the source-of-truth unless the user explicitly says otherwise.
- If the source language is ambiguous, ask once. Otherwise assume English.
- Keep section order aligned with the source README. Only make a small heading wording adjustment when needed to produce a valid localized anchor.
- Output localized siblings with `README.<bcp47-tag>.md` naming unless the repo already has a different established pattern that should be preserved.
- Update an existing language selector in place. Do not duplicate it.
- Translate only human-language content.
- Preserve project names, package names, commands, CLI flags, option names, environment variables, URLs, file paths, inline code, code fences, HTML attributes, and badge/image URLs.
- Badge alt text or visible labels may be translated only when the change does not require changing the badge URL, query params, or image source.
- If a glossary or do-not-translate list is provided, apply it consistently across every target language.
