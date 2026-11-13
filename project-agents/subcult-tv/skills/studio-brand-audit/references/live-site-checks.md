# Live-site checks

Run these against a deployed product site. Record the URL, capture time and viewport with each finding.

## Capture

Capture the page at 1440 and 390 pixels wide in a headless browser after its scripts settle. Save the served HTML and its same-origin CSS and JavaScript beside the captures; most checks below are searches in those files. Capture the live page again before calling a finding fixed; a merged change may not be deployed. When the page shows an error or an empty state, log its network requests and name the one that fails: Arkhiv showed "temporarily unavailable" while its catalog requests returned 200 and only the session request returned 404.

## Identity

- **Fonts:** every family the CSS names has an `@font-face` rule and a file that loads. A `font-family` line alone falls back to system fonts.
- **Colors:** the CSS values match the pack's `tokens.json`. List each value the pack lacks.
- **Header mark:** the pack's own mark, rather than a typed monogram or the source's logo.
- **Favicon:** `/favicon.ico` returns 200, and the pack passes `studio/brand-tools/check_pack_quality.py`.
- **Default theme:** the color scheme a first visitor gets shows the identity, and `theme-color` follows each scheme.
- **Stronger site:** when the site's identity is stronger than its pack, record a pack gap for `create-subcult-branding` rather than asking the site to step down.

## Head and sharing

- `<title>`, description, canonical, `og:*` and `twitter:*` tags sit in the served HTML.
- `og:image` is absolute, returns 200 and is 1200×630; `og:title` says what the product is.
- The pre-rendered headline and the one the app renders agree.

## First screen and copy

- The first screen says what the product is, also when the root opens into the app, a sign-in form, a data table or an empty listing.
- Visitors see finished copy: raw filenames as titles, record IDs, internal notes, debug strings and repeated placeholder tiles are findings.
- One product name runs through the title, header, share tags, README, release files and API responses.
- Copy follows `studio/content/VOICE.md`, including its list of repeated shapes such as stacked two-fragment headlines. Cookie and consent text is copy too.
- The page states maturity (pilot, preview, alpha) where the README does.
- An archive of someone else's work carries a not-endorsed line on the site and uses its own mark in the header.

## Repository and docs

- The README opens with the pack's lockup or banner and a one-line pitch; the description and topics are plain and current.
- The repository holds no local absolute paths, stray screenshots or retired product names.
- Releases carry notes a user can read, on the host that is now the source.
- The pack's `WEBSITE.md` and `GUIDE.md` match the live site and name the observation date; `VOICE.md` has a section for the product.

## Scoring and ranking

When asked to score or rank products, score each part out of 10 and weight them: identity 30%, live site 25%, pack alignment 15%, copy 15%, design system and repository 15%. Keep 9 and 10 for work that holds up beside the best pack. Show the rubric with the ranking, and choose redesign candidates by what a redesign would gain, which is a separate list from the lowest scores.
