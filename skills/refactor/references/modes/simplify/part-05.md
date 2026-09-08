## Process

### Step 1: Understand Before Touching

Before changing or removing anything, understand why it exists.

Answer:

- What is this code's responsibility?
- What calls it? What does it call?
- What are the edge cases and error paths?
- Are there tests that define expected behavior?
- Why might it have been written this way?

If you can't answer these, read more context first.

### Step 2: Look for Simplification Opportunities

Signals:

- Deep nesting
- Long functions with mixed responsibilities
- Nested ternaries
- Boolean flag arguments
- Repeated conditionals
- Generic or misleading names
- Duplicated logic
- Dead code
- Wrappers or abstractions that add no value

### Step 3: Apply Changes Incrementally

Make one simplification at a time.

For each simplification:

1. Make the change
2. Run relevant tests
3. Keep it only if behavior is preserved

Separate refactoring from feature work whenever possible.

### Step 4: Verify the Result

After simplifying, confirm:

- The code is genuinely easier to understand
- The diff is clean and reviewable
- Project conventions still match
- No behavior, error handling, or side effects changed
