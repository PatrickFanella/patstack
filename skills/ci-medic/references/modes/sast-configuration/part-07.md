## Common Use Cases

### New Project Setup

```bash
./scripts/run-sast.sh --setup --language python --tools semgrep,sonarqube
```

### Custom Rule Development

```yaml
# See references/semgrep-rules.md for detailed examples
rules:
  - id: hardcoded-jwt-secret
    pattern: jwt.encode($DATA, "...", ...)
    message: JWT secret should not be hardcoded
    severity: ERROR
```

### Compliance Scanning

```bash
# PCI-DSS focused scan
semgrep --config p/pci-dss --json -o pci-scan-results.json
```
