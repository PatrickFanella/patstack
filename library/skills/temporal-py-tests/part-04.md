## Available Resources

This skill provides detailed guidance through progressive disclosure. Load specific resources based on your testing needs:

### Unit Testing Resources

**File**: `resources/unit-testing.md`
**When to load**: Testing individual workflows or activities in isolation
**Contains**:

- WorkflowEnvironment with time-skipping
- ActivityEnvironment for activity testing
- Fast execution of long-running workflows
- Manual time advancement patterns
- pytest fixtures and patterns

### Integration Testing Resources

**File**: `resources/integration-testing.md`
**When to load**: Testing workflows with mocked external dependencies
**Contains**:

- Activity mocking strategies
- Error injection patterns
- Multi-activity workflow testing
- Signal and query testing
- Coverage strategies

### Replay Testing Resources

**File**: `resources/replay-testing.md`
**When to load**: Validating determinism or deploying workflow changes
**Contains**:

- Determinism validation
- Production history replay
- CI/CD integration patterns
- Version compatibility testing

### Local Development Resources

**File**: `resources/local-setup.md`
**When to load**: Setting up development environment
**Contains**:

- Docker Compose configuration
- pytest setup and configuration
- Coverage tool integration
- Development workflow
