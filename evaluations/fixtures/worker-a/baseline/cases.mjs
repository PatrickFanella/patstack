import assert from 'node:assert/strict';

// Case 1: a TSX-like component fixture. The requested rename is `total` -> `visibleTotal`.
export const cartSummaryBefore = `export function CartSummary({ items }: { items: string[] }) {\n  const total = items.length;\n  return <p>{total} items</p>;\n}`;
export const cartSummaryAfter = `export function CartSummary({ items }: { items: string[] }) {\n  const visibleTotal = items.length;\n  return <p>{visibleTotal} items</p>;\n}`;

// Case 2: desired lifecycle boundary.
export const lifecycleType = `type Lifecycle =\n  | { kind: 'idle' }\n  | { kind: 'running'; attempt: number }\n  | { kind: 'failed'; message: string }\n  | { kind: 'complete'; resultId: string };`;

// Cases 4 and 6: acceptance criteria: trim input; reject blank input; retry one transient failure.
export function normalizeLabel(input) {
  const value = input.trim();
  if (!value) throw new Error('label is required');
  return value;
}

export async function retryOnce(operation) {
  try { return await operation(); }
  catch (first) { return operation(); }
}

// Case 5: endpoint contract fixture.
export function healthEndpoint() {
  return { status: 200, body: { ok: true, version: '1.0.0' } };
}

// Case 7: successful process execution is not application success when it returns an error envelope.
export function helperSucceeded(result) {
  return result.exitCode === 0 && !result.stdout.error;
}

assert.match(cartSummaryAfter, /visibleTotal/);
assert.doesNotMatch(cartSummaryAfter, /const total/);
assert.match(lifecycleType, /\{ kind: 'failed'; message: string \}/);
assert.equal(normalizeLabel('  alpha '), 'alpha');
assert.throws(() => normalizeLabel('   '), /required/);
let attempts = 0;
assert.equal(await retryOnce(async () => { attempts += 1; if (attempts === 1) throw new Error('transient'); return 'ok'; }), 'ok');
assert.equal(attempts, 2);
assert.deepEqual(healthEndpoint(), { status: 200, body: { ok: true, version: '1.0.0' } });
assert.equal(helperSucceeded({ exitCode: 0, stdout: { error: { code: 'UPSTREAM' } } }), false);
console.log(JSON.stringify({ ok: true, cases: [1, 2, 4, 5, 6, 7] }));
