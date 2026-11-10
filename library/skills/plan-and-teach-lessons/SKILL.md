---
name: plan-and-teach-lessons
description: Plan or teach a course, tutor a concept, scaffold requested exercises
  or review learning progress.
metadata:
  argument-hint: What would you like to learn about?
---

# plan-and-teach-lessons

Select planning, tutoring, course delivery, exercise scaffolding or retrospective. Help the learner build understanding; use course-specific repository formats only when the target uses them.

Select the matching procedure below and load only that procedure and its needed resources. Each procedure retains its own client, tool and invocation limits. Internal handoffs use the matching procedure below rather than reloading this entrypoint. A reference does not authorize delegation, publication, deployment or an unrelated mutation.

- **lesson workspace**: Teach: run a multi-session course on a topic in the current workspace, with a mission, lessons, reference sheets and learning records. Use for /teach or 'teach me X'. Read [the procedure](references/base-workflow.md).
- **learning roadmap**: Learning roadmap: plan a multi-session path through a topic with milestones, practice exercises and progress checkpoints. Read [the procedure](references/modes/learning-roadmap/guide.md).
- **patient tutor**: Teaching: explain a concept or coach someone who is struggling so they build the understanding themselves. Read [the procedure](references/modes/patient-tutor/guide.md).
- **learning retro**: Retrospect on a learner's milestone: compare work to goals, find blockers and weak concepts, adjust pacing and the next checkpoint. Use after a study milestone. Read [the procedure](references/modes/learning-retro/guide.md).
- **exercise scaffold**: Scaffold course exercises (problem/solution/explainer folders, readmes) that pass `pnpm ai-hero-cli internal lint`. Use when stubbing or renumbering exercises in an AI Hero-format course repo. Read [the procedure](references/modes/exercise-scaffold/guide.md).

Read [conditional companions](references/skill-routes.md) only when their stated condition applies.
