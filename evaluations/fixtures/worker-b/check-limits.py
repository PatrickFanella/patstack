from pathlib import Path

text = Path(__file__).with_name("app.yaml").read_text()
for expected in ('cpu: "100m"', 'memory: "128Mi"', 'cpu: "250m"', 'memory: "256Mi"'):
    if expected not in text:
        raise SystemExit(f"missing {expected}")
print("resource limits fixture check passed: requests 100m/128Mi, limits 250m/256Mi")
