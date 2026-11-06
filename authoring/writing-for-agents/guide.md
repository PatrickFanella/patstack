# Writing for agents

This guide covers any document an agent consumes: a skill, an `AGENTS.md` or `CLAUDE.md`, or a doc reached by a pointer. The packaging differs; the writing does not. The same levers make each one predictable, so the agent takes the same _process_ every run rather than producing the same output. When the document is a skill, also read [`SKILL-MECHANICS.md`](SKILL-MECHANICS.md) for frontmatter, invocation choice and router skills.

Read the parts whose trigger matches the edit:

- [Context pointers](part-02.md): read when writing or changing a skill description, an `AGENTS.md` line, or any link that decides when an agent reaches other material.
- [The two loads](part-03.md): read when deciding whether new material should be always loaded, behind a pointer, or left to the human.
- [Information hierarchy](part-04.md): read when deciding what stays in the main file and what moves to a reference, or when a document has grown long.
- [Steps and completion criteria](part-05.md): read when writing ordered steps, or when an agent ends a step too early.
- [When to split](part-06.md): read before splitting one document into two, or merging two into one.
- [Leading words](part-07.md): read when the same idea is spelled out at several sites, or when an instruction is phrased as a prohibition.
- [Pruning](part-08.md): read when reviewing an existing document for duplication, stale lines or instructions that change nothing.
