## Workflow

### 1. Establish the source README and languages

- Confirm the source README path. Default to `README.md`.
- Identify the source language from the file contents and repo context.
- Determine target languages from the request or existing repo pattern.
- Note any glossary terms, product names, or phrases that must stay untranslated.

### 2. Audit the Markdown structure before translating

Read the source README once as structure, not prose. Open [`references/preservation-checklist.md`](./references/preservation-checklist.md) and inventory the elements most likely to break:

- headings and heading levels
- badge rows, shields URLs, and image links
- tables and alignment rows
- raw HTML blocks and inline HTML
- GitHub alerts or admonitions such as `> [!NOTE]`
- code fences, inline code, commands, and config snippets
- intra-document anchors such as `(#installation)`
- relative links to files, docs, screenshots, or other README variants

If the README already has localized siblings, inspect them too before choosing filenames or selector style.

### 3. Translate only the prose layer

Translate:

- paragraph text
- list item prose
- table cell prose
- visible text inside HTML blocks
- image alt text when safe
- selector labels and other human-facing labels

Do not translate:

- fenced code blocks
- inline code spans
- shell commands
- flags such as `--help`
- env vars such as `OPENAI_API_KEY`
- URLs
- file paths
- repo/package/project identifiers
- badge and image URLs

When in doubt, preserve the literal token and translate the surrounding sentence instead.

### 4. Preserve structure while writing the localized README

- Keep the same heading hierarchy and section order as the source.
- Keep the same number of code fences unless the user explicitly asks to rewrite examples.
- Preserve table shape, list nesting, HTML wrappers, and Markdown comments.
- Preserve relative links unless a link intentionally needs to point at a localized sibling README.

### 5. Rewrite localized anchors and anchor-dependent links

When a translated heading changes, GitHub will generate a different heading ID. After translating headings:

- rewrite every same-file `(#...)` link so it matches the localized heading slug in that file
- preserve custom explicit anchors such as `<a id="...">` unless the file already uses localized explicit IDs
- verify that every intra-document anchor target resolves to an existing heading or explicit anchor

Prefer a small heading wording adjustment over a broken anchor. The section order should still match the source README.

### 6. Write sibling files using the repo's naming pattern

Default to sibling filenames like:

- `README.zh.md`
- `README.es.md`
- `README.fr.md`

If the repo already uses a different multilingual naming pattern, keep using it consistently rather than forcing the default pattern.

### 7. Insert or update the language selector

Open [`references/language-selector-reference.md`](./references/language-selector-reference.md) before editing selectors.

Placement:

- keep the selector near the top of the file
- if the README starts with a title, badges, hero image, or short intro block, place the selector immediately after that opening cluster

Behavior:

- update an existing selector block in place if one already exists
- if you add a new selector, use the canonical marker comments from the reference file so later runs can update it deterministically
- emphasize the current language and link the other variants
- keep selector order and labels consistent across every README variant

### 8. Final verification

Before finishing, verify:

- localized filenames follow the chosen pattern
- every README variant contains exactly one selector block
- code fence counts are preserved
- badge/image URLs and relative file links still point to the original targets unless intentionally localized
- every `(#...)` link resolves inside its own file
- the localized README still feels structurally identical to the source
