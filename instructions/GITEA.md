# Gitea agent identity

Use `subcult-agent` for agent actions on `https://git.subcult.tv` on every device. The default `tea` login and Gitea HTTPS Git credential helper select this account. When a command accepts a login, pass `--login subcult-agent`; names such as `open-pilot`, `subcult`, and `patrickfanella` may still authenticate as the human operator.

Before a Gitea write, verify `tea api --login subcult-agent /user` returns `login: subcult-agent`. Before committing agent work, inspect `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT`. Gitea repositories normally inherit `SUBCULT Agent <info@subcult.tv>` from a conditional Git include. If a worktree or environment overrides it, use command-local `-c user.name='SUBCULT Agent' -c user.email='info@subcult.tv' -c commit.gpgsign=false` for the agent commit. Do not sign agent commits with the human operator's key.

Use the installed Gitea HTTPS credential helper for pushes. Fleet Git URL rules route Gitea SSH remotes through HTTPS without changing repository remotes. Do not bypass these rules with a human SSH key or recover a permission failure by falling back to a human token. Report the missing access and obtain the appropriate repository grant.

The account has code, issue and pull request write access to the 69 `subculture-collective` repositories enrolled on October 3, 2026, plus Actions read access. Future repositories and other owners require explicit enrollment. The account is not a site administrator or organization owner. Administrator work needs the user's authorization and an explicitly selected administrative identity.

Device tokens are stored in private `tea` configuration. Do not print them, put them in remote URLs, copy them into project files, or revoke retained human/service credentials during routine agent work. Configuration deployment and rollback receipts live in `~/.local/state/gitea-agent/` on each host. Existing running services with explicit credentials are separate consumers; changing CLI defaults does not migrate their credentials.
