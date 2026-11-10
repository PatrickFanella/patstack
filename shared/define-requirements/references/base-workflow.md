# Base procedure

Reviewed source clients: codex, claude.

Resolve command and resource paths from the owning skill root, unless a linked reference says otherwise.

# define-requirements

Resolve only the ambiguity that blocks a safe decision. This workflow combines
the former `grill-me`, `grill-with-docs`, and define-requirements skills.

## Requested grilling

When the user says `grill-me`, `grill-with-docs`, or asks to stress-test a plan, read [the grilling procedure](grilling.md). Use the bounded workflow below for ordinary clarification. The named mode stays here so it shares one owner with requirements discovery.

## Workflow

1. Inspect available code, documents, issue context, and conventions first.
2. Write down the intended outcome, known constraints, and unresolved choices.
3. Ask at most five focused questions. Ask fewer when one answer will unblock the
   work, and do not ask the user for facts available in the environment.
4. Prefer a short set of concrete options when the tradeoff is well understood.
   Explain the recommended option and allow a free-form answer.
5. Restate the agreed scope, non-goals, acceptance criteria, and verification.
6. Route directly to implementation when the work is bounded. Use a written plan
   when decisions span multiple steps, affect public contracts, or are costly to
   reverse.

## Interview Lenses

Use only the lenses relevant to the request:

- Outcome: what observable result should exist?
- Scope: what is explicitly included or excluded?
- Constraints: compatibility, security, performance, timing, or tool limits?
- Contracts: APIs, schemas, migrations, data, privacy, or user-visible behavior?
- Evidence: what tests, examples, or measurements prove completion?
- Tradeoffs: which choice materially affects maintainability or risk?

## Deliverable

Before handoff, capture:

```markdown
Goal:
In scope:
Out of scope:
Constraints and decisions:
Acceptance criteria:
Verification:
Open questions:
Recommended route: direct | lightweight plan | full plan
```

Use `templates/adr-format.md` when a durable decision record is warranted and
`templates/context-format.md` for a larger discovery handoff. The original
grilling workflow is retained as optional background in
`references/curated/grill-me.md`.

## Retained brainstorming resources

Load `references/curated/brainstorming.md` only when a requirements interview
needs the retained brainstorming guidance. No brainstorming scripts were
retained; follow the guidance as prose.

## Guardrails

- Do not turn every request into an interview.
- Do not require approval for reversible implementation details already covered
  by the user's request.
- Do not dump a questionnaire or repeatedly ask equivalent questions.
- Stop interviewing as soon as the remaining assumptions are safe and explicit.
