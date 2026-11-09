# temporal-py-tests procedure

Reviewed source clients: claude, codex, opencode. Check the actual client tools before following this procedure. Resolve its scripts, references and assets from this directory, not from the outer skill root.

# temporal-py-tests

Test Temporal Python workflows with replay, time skipping, activities, mocks, and determinism checks.

## Testing Philosophy

**Recommended Approach** (Source: docs.temporal.io/develop/python/testing-suite):

- Write majority as integration tests
- Use pytest with async fixtures
- Time-skipping enables fast feedback (month-long workflows → seconds)
- Mock activities to isolate workflow logic
- Validate determinism with replay testing

**Three Test Types**:

1. **Unit**: Workflows with time-skipping, activities with ActivityEnvironment
2. **Integration**: Workers with mocked activities
3. **End-to-end**: Full Temporal server with real activities (use sparingly)

## Key Testing Principles

1. **Time-Skipping** - Month-long workflows test in seconds
2. **Mock Activities** - Isolate workflow logic from external dependencies
3. **Replay Testing** - Validate determinism before deployment
4. **High Coverage** - ≥80% target for production workflows
5. **Fast Feedback** - Unit tests run in milliseconds

## Coverage Targets

**Recommended Coverage** (Source: docs.temporal.io best practices):

- **Workflows**: ≥80% logic coverage
- **Activities**: ≥80% logic coverage
- **Integration**: Critical paths with mocked activities
- **Replay**: All workflow versions before deployment

## Resources

- [Integration testing](resources/integration-testing.md): read when mocking activities, injecting errors, or testing signals and queries.
- [Local setup](resources/local-setup.md): read when setting up a local Temporal server, pytest configuration or coverage tooling.

Unit-test and replay-test resources are not bundled. Start unit tests from the [quick start](part-05.md), and take replay patterns from the Python SDK testing docs below.

## Additional References

- Python SDK Testing: docs.temporal.io/develop/python/testing-suite
- Testing Patterns: github.com/temporalio/temporal/blob/main/docs/development/testing.md
- Python Samples: github.com/temporalio/samples-python

Read only the [task guide](guide.md) entries whose trigger matches the work.

Keep the requested scope and repository conventions. Report evidence for the operation actually performed.
