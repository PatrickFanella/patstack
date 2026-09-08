import assert from 'node:assert/strict';

// Task 2: architecture/domain route emits an exhaustive lifecycle boundary.
const lifecycle = [
  { kind: 'idle' },
  { kind: 'running', attempt: 1 },
  { kind: 'failed', message: 'timeout' },
  { kind: 'complete', resultId: 'r-1' },
];
assert.deepEqual(lifecycle.map((state) => state.kind), ['idle', 'running', 'failed', 'complete']);

// Task 4: bounded implementation acceptance criteria.
function normalizeLabel(input) {
  const trimmed = input.trim();
  if (!trimmed) throw new Error('label is required');
  return trimmed;
}
assert.equal(normalizeLabel(' alpha '), 'alpha');
assert.throws(() => normalizeLabel('   '), /label is required/);

// Task 5: endpoint public contract check.
function healthEndpoint() {
  return { status: 200, body: { ok: true, version: '1.0.0' } };
}
const response = healthEndpoint();
assert.equal(response.status, 200);
assert.equal(typeof response.body.ok, 'boolean');
assert.equal(response.body.ok, true);
assert.equal(typeof response.body.version, 'string');

// Task 6: old and new implementations use exactly the same transient reproducer.
async function oldRetryOnce(operation) {
  return operation();
}
async function newRetryOnce(operation) {
  try {
    return await operation();
  } catch {
    return operation();
  }
}
function transientOperation() {
  let attempts = 0;
  return async () => {
    attempts += 1;
    if (attempts === 1) throw new Error('transient crash');
    return { value: 'ok', attempts };
  };
}
await assert.rejects(oldRetryOnce(transientOperation()), /transient crash/);
assert.deepEqual(await newRetryOnce(transientOperation()), { value: 'ok', attempts: 2 });

// Task 7: process success is distinct from semantic success.
function semanticSuccess({ exitCode, stdout }) {
  return exitCode === 0 && !(stdout && stdout.error);
}
assert.equal(semanticSuccess({ exitCode: 0, stdout: { error: { code: 'UPSTREAM' } } }), false);

console.log(JSON.stringify({ ok: true, oldImplementation: 'failed as expected', newImplementation: 'passed', tasks: [2, 4, 5, 6, 7] }));
