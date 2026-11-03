# Example Play Loop Prompt

Use `play-edda` to choose the next turn.

Inputs available:

- Base URL: `https://edda.subcult.tv`
- Campaign ID: `<campaign-id>`
- Auth token is available in `EDDA_TOKEN`

Workflow:

1. Fetch turn context:
   ```bash
   python3 <play-edda skill dir>/scripts/edda_api.py turn-context <campaign-id>
   ```
2. Read recent history, location, quests, character, NPCs, facts, and time.
3. Choose one safe, quest-progressing action.
4. Submit it:
   ```bash
   python3 <play-edda skill dir>/scripts/edda_api.py action <campaign-id> "<action>"
   ```
5. Report action, outcome, next pressure, play score, and issues.

If no token/campaign is available, stop and ask for it. Do not invent state.
