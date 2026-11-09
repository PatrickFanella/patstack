# terraform-module-smith procedure

Reviewed source clients: claude, codex, opencode. Check the actual client tools before following this procedure. Resolve its scripts, references and assets from this directory, not from the outer skill root.

# terraform-module-smith

Create reusable Terraform modules with explicit inputs, provider constraints, examples, and validation.

## Standard Module Pattern

```
module-name/
├── main.tf          # Main resources
├── variables.tf     # Input variables
├── outputs.tf       # Output values
├── versions.tf      # Provider versions
├── README.md        # Documentation
├── examples/        # Usage examples
│   └── complete/
│       ├── main.tf
│       └── variables.tf
└── tests/           # Terratest files
    └── module_test.go
```

## Best Practices

1. **Use semantic versioning** for modules
2. **Document all variables** with descriptions
3. **Provide examples** in examples/ directory
4. **Use validation blocks** for input validation
5. **Output important attributes** for module composition
6. **Pin provider versions** in versions.tf
7. **Use locals** for computed values
8. **Implement conditional resources** with count/for_each
9. **Test modules** with Terratest
10. **Tag all resources** consistently



The Terratest pattern runs `terraform apply` and `destroy` against a real provider account. Run it only in an account the user designated for tests.

Read only the [task guide](guide.md) entries whose trigger matches the work.

Keep the requested scope and repository conventions. Report evidence for the operation actually performed.

## Companion skills

Load [required steps and optional helpers](references/skill-routes.md) only when their stated condition applies.
