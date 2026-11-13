# Product launch workflow

Take one SUBCULT product from no identity to an owner-selected brand, a marketing packet and a small product site. Pult is the worked example: `studio/studies/theme-tender-directions/` for the review, `studio/brands/pult/` for the pack, and `site/` plus `deploy/` in `subculture-collective/pult` for the site.

Work from a worktree on current `origin/main` when the `subcult-tv` checkout is dirty or behind; recent packs and studies are missing otherwise. The canonical checkout is on Kvant, so from another host work there over SSH rather than cloning. `studio-brand-handoff`, `studio-brand-audit` and `social-craft` are selected only inside `subcult-tv`; read them from its `.agents/skills/` when your session started elsewhere.

| Stage | Output | Ends when |
| --- | --- | --- |
| 1. Facts | Claims register entries, voice section | Sources are read |
| 2. Board | Twelve references, three or four mixed directions | **The owner has the board. Stop here.** |
| 3. Rounds | `round-N/` boards | The owner names a direction or mix, mark, palette and type |
| 4. Pack | `studio/brands/<slug>/` | Exports render and trace to sources |
| 5. Marketing | `docs/marketing/` in the product repository | Every claim has a source |
| 6. Site | `site/` and `deploy/` in the product repository | Local checks pass |
| 7. Handoff | One PR per repository | CI is green and each PR merges cleanly |

The owner's decision in stage 3 authorizes stages 4 to 7 as one run. Continue through them without another pause.

## 1. Facts

Read the product's README, source, license and release state. Add what it can truthfully claim to `studio/content/social/Product Claims Register.md`. Read `studio/content/VOICE.md`, including its list of repeated shapes to avoid, and add a voice section for the product. Read `studio/brands/README.md` so the new identity can be checked against every existing pack.

## 2. Board

Write `studio/studies/<product>-directions/` with `README.md`, `index.html` and `sources.json`.

Screen the 1,342 Refero exports and the curated studies listed in `studio/references/catalog.json`, the same records the admin library shows. Each `refero-archive/styles/<id>/DESIGN.md` has token tables, measured type and font substitutes. Catalog tags are keyword guesses, so filter the token tables by script down to about 40 candidates and read those against what the product needs. Keep twelve unless the owner asks for another number. `sources.json` records each style ID, source URL, screenshot hash and archive path.

The board has these parts, in order:

1. **Brand rule under test:** one sentence drawn from how the product behaves, with a pointer to the code or docs that show it.
2. **Twelve references,** grouped by the idea each group contributes. Each shows its name, source link, what to borrow, palette swatches, type with an OFL substitute, and the private screenshot.
3. **Three or four mixed directions.** Each names the references it mixes and shows an original mark, a house palette with roles and measured contrast, a type pairing, and the same sample content as the others: landing hero, docs excerpt and social card, at wide and phone widths.
4. **Palette examples:** each house palette applied to real text, button and panel pairs. Where the product displays color itself, add a switcher that re-tints the directions.
5. **Mix table:** palette, type, layout, mark and motif by source, so the owner can answer "B's palette with D's type".
6. **Recommendation and collisions:** the pick, why, and every overlap with an existing pack.
7. **Limits:** which fonts still need licences in `studio/brand-tools/fonts/`, what is illustrative, and that nothing is selected.

Keep the board private, since reference screenshots grant no reuse rights. Put it where the owner can open it from another device: a private page when the client can publish one, otherwise the path and local preview command. Record the link in the study's README. End the turn with the board, the recommendation and what you need decided.

## 3. Rounds

Build each later round in `round-N/index.html` and leave earlier rounds intact. Add a dated README section with what the owner asked for and what changed. A round can narrow, push a direction further, or test names, marks, type and in-use mock-ups. When names are in play, check package registries and state that this is not a trademark search.

Record the outcome in the study's README with the date and the owner's choice, including how a mix was combined.

## 4. Brand pack

Follow Document and Produce in [the workflow](workflow.md). `studio/brands/pult/` with its `brand.json` and `build.py` is the current model for a standalone pack. Carry the recorded choice into `brand.json` (`direction_selection`, `mark_status`). Draw the signature scene and the 16-pixel favicon from [the workflow](workflow.md) before the social layouts, since every layout is built around the scene. Add the selected fonts with their OFL texts, add a row to `studio/brands/README.md`, and keep `asset_status` pending. Approval for website use and for social posts are separate owner decisions.

## 5. Marketing

Copy `studio/brand-tools/starter-template/marketing/` to `docs/marketing/` in the product repository, complete `context.md` and `packet.md` there, and link them from the pack. If the starter also put a copy in the pack, remove it so one packet stays editable. The clpr and Subsets repositories have finished examples. Fill the channels that fit the product: positioning, short and long descriptions, launch post, release note, demo brief and 30-day plan.

Replace the pack's sample layout copy with lines from the packet, then rebuild that brand alone. Each claim traces to the register. Captures use real product output with synthetic data; label anything mocked. Use `social-craft` for individual posts. Everything stays a draft: nothing is scheduled, sent or posted.

## 6. Product site

Build static HTML with no build step or backend, in the product repository. Match Pult's structure and level of finish. Take the look and the page's central idea from the new brand, in the way Pult's remote and channel framing comes from its own. Use `<slug>.subcult.tv` as the canonical URL unless the product has its own domain.

| Path | Contents |
| --- | --- |
| `site/index.html` | Title, description, canonical, Open Graph and Twitter tags; skip link; nav with Docs, Install, Git and Support; hero stating what the product does with two actions; a real demo or one labelled as a mock-up; what it covers, with counts from source; install section stating maturity honestly; one support block; footer |
| `site/docs/index.html` | On-this-page nav; install; first run; commands, flags or keys; configuration; undo or recovery where relevant; a More section linking source, issues, project docs, contributing and security |
| `site/404.html` | `noindex`, in the product's voice, links to home and docs |
| `site/style.css` | Pack tokens mapped to named variables |
| `site/app.js` | Demo and copy buttons only; the page reads fully without it |
| `site/assets/`, `site/fonts/` | Marks and `og.png` mapped through `studio-brand-handoff`; Latin-subset WOFF2 files with their OFL texts |
| `site/robots.txt`, `site/sitemap.xml` | Canonical product URL |
| `site/README.md` | Preview command, the source file behind each fact, and where the brand assets came from |
| `deploy/` | Dockerfile on `nginx-unprivileged`, `nginx.conf`, `compose.yml` and `<product>.Caddyfile`, modeled on Pult's |

The footer links docs, the source repository (GitHub `subculture-collective/<name>` for organization repositories; Gitea for a repository that exists only there), support and `https://subcult.tv`, and carries the licence line. Follow `studio/content/patreon/support-redesign-2026-10/site-guidelines.md` for support: link `https://subcult.tv/support` by default, or Patreon directly from a block that names SUBCULT; one block after the explanation or demo, a quiet footer link, no prices or tiers, and no ask on the error page.

Every command, flag, key and count comes from the product's source. Preview the site locally and check 360 and 1280 pixel widths for overflow, console errors, font loading, keyboard use, contrast, the demo and every link. Font loading means an `@font-face` rule for every family the CSS names; a `font-family` line alone falls back to system fonts, which happened on Kork, Left Field and Dedhed. Serve `/favicon.ico` beside the SVG icons. Run `studio-brand-audit` against the pack.

## 7. Handoff and deployment

Open one PR in `subcult-tv` for the study, pack and claims, and one in the product repository for the site, deploy files and marketing. Report the links, the selection record, checks run and what remains for the owner.

Deploy only when the request says to and the owner has approved the assets for website use. Deployment changes Almaz's shared Caddy, so follow `50-reports/Pult website deployment 2026-11-08.md` in Machinum. It is done when served files match the source commit by hash, the live URL passes at both widths and neighboring sites still respond.
