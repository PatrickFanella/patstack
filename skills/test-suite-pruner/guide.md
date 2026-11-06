# test-suite-pruner steps

The rules in `SKILL.md` apply to every step. Take the steps in order; paths are relative to this directory, and the target repository is passed explicitly.

1. [Establish the actual baseline](part-02.md): read first, before any edit, to record repository state and baseline results.
2. [Remove with evidence](part-03.md): read when classifying and removing generated output, documents, code, dependencies, tests or an external integration.
3. [Reshape tests around contracts](part-04.md): read when consolidating or rewriting tests, or choosing which layer should own a behavior.
4. [Make the result maintainable](part-05.md): read when adding or repairing gates, or before any coverage-threshold change.
5. [Verify and finish](part-06.md): read before the final broad run and the report.
