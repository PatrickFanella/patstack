# SAST configuration

Static Application Security Testing (SAST) tool setup, configuration, and custom rule creation with Semgrep, SonarQube and CodeQL: CI/CD scanning, custom rules, quality gates, false-positive tuning.

Paths here are relative to this mode directory; pass the target repository explicitly.

## Quick Start

### Initial Assessment

1. Identify primary programming languages in your codebase
2. Determine compliance requirements (PCI-DSS, SOC 2, etc.)
3. Choose SAST tool based on language support and integration needs
4. Review baseline scan to understand current security posture

### Basic Setup

```bash
# Semgrep quick start
pip install semgrep
semgrep --config=auto --error

# SonarQube with Docker
docker run -d --name sonarqube -p 9000:9000 sonarqube:10.8-community

# CodeQL CLI setup
gh extension install github/gh-codeql
codeql database create mydb --language=python
```

## Best Practices

1. **Start with Baseline**
   - Run initial scan to establish security baseline
   - Prioritize critical and high severity findings
   - Create remediation roadmap

2. **Incremental Adoption**
   - Begin with security-focused rules
   - Gradually add code quality rules
   - Implement blocking only for critical issues

3. **False Positive Management**
   - Document legitimate suppressions
   - Create allow lists for known safe patterns
   - Regularly review suppressed findings

4. **Performance Optimization**
   - Exclude test files and generated code
   - Use incremental scanning for large codebases
   - Cache scan results in CI/CD

5. **Team Enablement**
   - Provide security training for developers
   - Create internal documentation for common patterns
   - Establish security champions program

## Rollout order

1. Complete initial SAST tool setup
2. Run baseline security scan
3. Create custom rules for organization-specific patterns
4. Integrate into CI/CD pipeline
5. Establish security gate policies
6. Train development team on findings and remediation

## Read when needed

- [Tool comparison](part-10.md): read when choosing between Semgrep, SonarQube and CodeQL.
- [Core capabilities](part-03.md): read when deciding which features of the chosen tool to configure.
- [Integration patterns](part-05.md): read when wiring a scan into CI or a pre-commit hook.
- [Common use cases](part-07.md): read for a new-project setup, a custom rule, or a compliance-focused scan.
- [Troubleshooting](part-08.md): read when scans are noisy, slow, or fail to integrate.
