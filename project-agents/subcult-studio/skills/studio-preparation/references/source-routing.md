# Studio source routing

**Canonical owner on Kvant:** `/home/onnwee/Work/Subcult/subcult-tv/studio`. The paths below are relative to that folder. Resolve another device's owner before using them.

**Checkout state.** Read the current Git status and branch, and preserve unrelated and concurrent work. The canonical checkout may be on another agent's feature branch, so compare against `origin/main` before trusting a file as current. Existing review worktrees are independent sources of proposed changes, not an instruction to reset or merge them.

**The old Studio repository.** `~/Work/Subcult/subcult-studio` was removed on October 5, 2026, and its uncommitted work was lost. Its committed history is on Gitea at `subculture-collective/subcult-studio`, which is archived. Worktrees under `~/.t3/worktrees/subcult-studio/` are orphaned file copies with no Git metadata. Do not recreate that path.

## Sources

- **Brand packs:** `branding/library/README.md` and `selected-directions.json`, then `brands/<actual-brand>/` for the guide, tokens and `asset-manifest.json`.
  - The product repository may own newer approved interface specifications. Inspect the pack's provenance and the actual product source before reconciling a discrepancy.
  - `branding/library/references/subcult-mark-master.svg` and `subcult-edited-layouts/` beside it preserve the user's masters.
  - Visual-system work follows `studio-brand-system`.
- **Public claims:** `content/social/Product Claims Register.md` and the owning product's current source and release evidence. Local preview, hosted CI, production and public release are separate states.
- **Voice:** `content/VOICE.md`. Post writing and its research corpus (`content/social/research/`) follow `social-craft`.
- **Editorial preparation:** `content/social/Social Posting Automation Plan.md` and the actual runner configuration for sources and current schedules. Imported templates do not establish a promised posting cadence.
- **Supporter offer:** `content/patreon/support-redesign-2026-10/` (README, site-guidelines and patreon-copy), now on subcult-tv main. Read it for the owner's no-schedule direction. Treat prices, copy and access as proposed until exact approval and live account readback establish them. Do not rewrite historical plans or apply a live offer from this pointer alone.
- **Planning:** the SUBCULT vault's Home/Focus notes and its existing Strategy, Products or Publishing notes. Use explicit cross-vault URI links, and keep pointers to Studio rather than another editable content master.

The prior brand-voice, visual-design and worldbuilding library folders are preserved as historical source. Their universal dark-mode prescription and mandatory mythic tone are not active product policy. Generic content-strategy, copywriting and launch methods remain optional. Local facts and authority come from the owners above.

## Preparation runtime on Kvant (October 5, 2026)

Check the live units and links before relying on this section.

- **Upstream digest:** Switchyard workflow `changemaker-daily-digest` (trigger `daily-changemaker-native`, 09:00 UTC) collects product activity and writes the digest that the social jobs read.
- **Instagram and website/Patreon:**
  - `changemaker-instagram.timer` runs at 09:20 UTC and `changemaker-publications.timer` at 09:25 UTC.
  - Both run from installed bundles. `~/.local/share/posting-dashboard/changemaker` is a symlink to `releases/<sha>`; `publications/studio` is an overlay.
  - To deploy, copy a release, swap the symlink and keep a dated directory under `recovery/`.
  - A merged source change is not live until it is deployed.
- **X and Bluesky:**
  - `social-posting-plan` (Monday 10:00 Chicago), `-radar` (08:45, 13:45 and 18:15) and `-review` (Sunday 16:00) are unit links that run straight from the canonical checkout. They use whatever branch it has checked out.
  - These jobs share `runner.lock`. A second job started while one runs returns `already_running` and does nothing, so start them one at a time.
- **State:** `~/.local/state/social-posting/` holds runs, drafts, receipts and locks. Never replace it from source.
- **Review:** drafts reach the authenticated review dashboard unapproved. Approval, scheduling and publication need the owner and provider readback.
