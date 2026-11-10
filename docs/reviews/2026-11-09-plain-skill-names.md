# Plain skill names and group review, 2026-11-09

Skill names now say what the skill does. Earlier coined names are retired with no aliases;
`catalog/retired-names.json` maps each one to its owner, and
`catalog/plain-names-2026-11-09.json` records this rename.

## Evidence

Core changes rest on 45 days of Kvant agent session logs (242 files), counting actual
`SKILL.md` reads and Skill tool calls, with retired names mapped to current owners and
patstack and subsets worktrees excluded. Earlier listing counts were inflated by catalog
text. A skill agents ignored while listed may still be useful, and skills outside core
are under-loaded because they are not listed. Other hosts were not sampled.

## Name changes

| Old name | New name |
|---|---|
| `agent-fanout-plan` | `coordinate-parallel-agents` |
| `api-contract-smith` | `build-apis` |
| `auth-gatekeeper` | `build-and-fix-auth` |
| `bash-script-craft` | `bash-scripts` |
| `behavior-proof` | `verify-implementation` |
| `binary-dissector` | `reverse-engineer-binaries-protocols` |
| `boundary-drafter` | `design-architecture` |
| `branch-doctor` | `diagnose-branching-stories` |
| `browser-workbench` | `control-browser-and-desktop` |
| `bug-tracer` | `fix-bugs` |
| `build-sequencer` | `plan-and-implement-changes` |
| `bus-factor-map` | `analyze-code-ownership` |
| `ci-medic` | `build-and-fix-ci` |
| `claim-verifier` | `verify-claims` |
| `claude-git-guardrails` | `claude-code-git-safety` |
| `cli-contract-smith` | `build-cli-tools` |
| `commit-recap` | `summarize-commits` |
| `conlang-forge` | `design-fictional-languages` |
| `cursor-sdk-builder` | `build-with-cursor-sdk` |
| `data-narrative` | `present-data-findings` |
| `dep-upgrade-pilot` | `upgrade-major-versions` |
| `diff-inspector` | `review-code-changes` |
| `docx-editor` | `docx-files` |
| `editorial-roadmap` | `plan-content-strategy` |
| `eval-bench` | `evaluate-llm-behavior` |
| `fiction-editor` | `edit-fiction` |
| `fleet-ops-router` | `manage-infrastructure` |
| `friction-miner` | `improve-workflow-from-sessions` |
| `game-fun-theory` | `improve-game-design` |
| `git-surgery` | `manage-git-and-prs` |
| `go-craft` | `golang` |
| `landing-page-cro` | `improve-conversion-rates` |
| `launch-dossier` | `prepare-product-launch` |
| `lead-pipeline-ops` | `manage-sales-pipeline` |
| `lesson-workspace` | `plan-and-teach-lessons` |
| `lyric-doctor` | `diagnose-song-lyrics` |
| `market-position-map` | `research-market-positioning` |
| `mcp-server-forge` | `build-mcp-servers` |
| `mcp-wire-tracer` | `fix-mcp-connections` |
| `name-forge` | `diagnose-and-generate-names` |
| `observe-tune-loop` | `check-and-tune-systems` |
| `obsidian-cli-driver` | `use-obsidian-cli` |
| `opencode-config-tuner` | `configure-opencode` |
| `opentui-screens` | `build-opentui-apps` |
| `page-copy-forge` | `write-and-adapt-copy` |
| `paid-media-plan` | `plan-ad-campaigns` |
| `pci-scope-check` | `pci-dss-compliance` |
| `pdf-render-check` | `pdf-files` |
| `perf-hotpath-probe` | `improve-performance` |
| `postgres-workbench` | `postgres` |
| `pptx-forge` | `slide-decks` |
| `primary-source-notes` | `research-with-sources` |
| `prose-unslop` | `write-plainly` |
| `python-uv-workbench` | `python-projects` |
| `ram-dump-sleuth` | `analyze-ram-dumps` |
| `raster-image-gen` | `generate-and-edit-images` |
| `react-render-tuner` | `react-and-nextjs` |
| `red-green-loop` | `test-driven-development` |
| `relay-baton` | `handoff-and-recall-work` |
| `repo-atlas` | `map-codebase` |
| `repo-research-trail` | `investigate-code` |
| `retrieval-pipeline` | `build-rag-pipelines` |
| `rn-expo-builder` | `react-native-expo` |
| `roadmap-slicer` | `manage-roadmaps-and-issues` |
| `rpg-game-master` | `run-rpg-sessions` |
| `runway-modeler` | `model-startup-finances` |
| `rust-ownership-async` | `rust` |
| `safe-refactor-pass` | `refactor-code` |
| `sales-collateral` | `create-sales-materials` |
| `scope-grill` | `define-requirements` |
| `search-rank-audit` | `improve-seo` |
| `secret-rotation-flow` | `manage-deployment-secrets` |
| `secure-code-audit` | `secure-web-code` |
| `sheet-wrangler` | `spreadsheet-files` |
| `skill-forge` | `manage-skills-and-plugins` |
| `skill-stack-router` | `find-and-load-skills` |
| `sonic-fingerprint` | `describe-artist-sound` |
| `story-dna-extractor` | `analyze-and-adapt-stories` |
| `story-workbench` | `develop-and-draft-fiction` |
| `strategy-backtester` | `backtest-trading-strategies` |
| `stride-threat-map` | `threat-modeling` |
| `stripe-billing-guard` | `manage-stripe-account` |
| `stripe-checkout-wiring` | `integrate-stripe-payments` |
| `studio-brand-system` | `create-subcult-branding` |
| `super-productivity-workflow` | `manage-super-productivity` |
| `telemetry-signal-forge` | `build-and-fix-observability` |
| `test-suite-pruner` | `clean-up-test-suites` |
| `tetrad-impact-lens` | `analyze-technology-impact` |
| `thinking-audit` | `diagnose-reasoning` |
| `ts-type-design` | `typescript` |
| `tv-candle-charts` | `tradingview-lightweight-charts` |
| `ui-craft` | `style-web-ui` |
| `userscript-workshop` | `build-userscripts` |
| `video-production-lab` | `create-videos` |
| `voice-ledger` | `build-writing-voice-guide` |
| `vscode-extension-lab` | `build-vscode-extensions` |
| `web-game-loop` | `build-web-games` |
| `world-bible` | `fictional-worldbuilding` |
| `writing-workbench` | `write-and-revise-nonfiction` |

Unchanged: `karakeep-bookmarks`, `privacy-controls`, `ralph-workflow`, `temporal-workflows`, `throwaway-prototype`.

## Group changes

- **build-agent-tools** (20 to 21): added `claude-code-git-safety`.
- **build-and-ship** (21 to 24): added `pci-dss-compliance`, `privacy-controls`, `secure-web-code`, `upgrade-major-versions`. removed `check-and-tune-systems`.
- **core** (37 to 26): removed `build-and-fix-observability`, `build-cli-tools`, `build-mcp-servers`, `design-architecture`, `fix-mcp-connections`, `map-codebase`, `privacy-controls`, `refactor-code`, `secure-web-code`, `upgrade-major-versions`, `verify-claims`.
- **creative-production** (11 to 9): removed `build-web-games`, `improve-game-design`.
- **data-and-decisions** (12 to 12): added `analyze-code-ownership`. removed `build-rag-pipelines`.
- **diagnose-and-repair** (20 to 15): removed `analyze-code-ownership`, `backtest-trading-strategies`, `integrate-stripe-payments`, `pci-dss-compliance`, `temporal-workflows`.
- **fiction-and-worlds** (13 to 11): removed `diagnose-song-lyrics`, `write-and-adapt-copy`.
- **mobile-and-interfaces** (12 to 13): added `improve-game-design`.
- **operate-homelab** (14 to 12): added `build-and-fix-observability`, `check-and-tune-systems`. removed `backtest-trading-strategies`, `claude-code-git-safety`, `integrate-stripe-payments`, `temporal-workflows`.
- **product-and-launch** (16 to 17): added `diagnose-and-generate-names`.
- **research-and-write** (17 to 16): removed `diagnose-and-generate-names`.

Core stays small because `find-and-load-skills` can load any specialist on demand. Skills
whose only group was core moved to `build-and-ship`.

## Companion links

The routing graph grew from 55 to 256 edges and now covers 95 of 104 skills. Nine skills
work alone: file helpers, single-tool wrappers and the router itself. A test pins that
list, the absence of coined words in names, and backticked references to retired names.

## Not changed

Project and vault skills, non-selectable library originals, mode folders under
`references/modes/`, the stored `<!-- roadmap-slicer:` issue marker and the default
`./world-bible` data directory keep their names.

## Rollout dependencies

Live consumers outside this repository name a skill directly and must change with the
fleet deployment:

- The social-posting jobs read `~/.codex/skills/prose-unslop/SKILL.md` directly
  (`radar.py`, `runner.py`, `craft.py`, `changemaker_instagram.py` in subcult-tv and the
  active posting-dashboard release). They must read the new `write-plainly` path first.
- Machinum's Agent Documentation Policy names `prose-unslop` as the required writing skill.
- Global agent instructions are regenerated from `scripts/global-instructions.py`.
- Existing agent sessions keep their old catalog until restarted.
