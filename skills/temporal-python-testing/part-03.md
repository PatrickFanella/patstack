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
