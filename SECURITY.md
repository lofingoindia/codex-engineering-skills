# Security policy

## Reporting a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/lofingoindia/codex-engineering-skills/security/advisories/new) for a suspected security problem. Do not put real credentials, customer data, private infrastructure, or exploit details in a public issue. Include the affected commit/release, skill or tool, reproducible steps using synthetic data, impact, and any proposed correction.

The maintainer will assess reports as capacity allows. There is no promised response SLA or bounty program. Coordinate disclosure through the private report before publishing sensitive details.

## Scope and supported revisions

Security fixes target the current maintained branch and future releases. Historical tags remain immutable; users on an affected tag must deliberately move to a corrected release. Backports are assessed case by case and are not guaranteed for every old revision.

The collection contains instructions and maintainer tooling. Skills cannot enforce backend authorization or replace application security review. Optional evaluation fixtures deliberately contain defects and must stay isolated from production. Review artifact code before running its checker.

## Installation safety

Read [installation and update safeguards](docs/installing-and-updating.md) before changing an existing installation. The tested Skills CLI does not protect local modifications, and its `check` command is mutating in version 1.7.4. Back up installed directories and tracking files before updates or removals. A version tag or source hash identifies content; it does not establish that the content is harmless.

## Repository controls

Public-fork checks use `pull_request`, read-only workflow permissions, no repository secrets, and GitHub-hosted runners. Do not replace this with privileged `pull_request_target` execution of contributor code. External actions and the upstream validator must remain reviewed and pinned. Dependabot and secret scanning are useful safeguards, not a substitute for review.

Do not commit `.tools/`, `.runs/`, archives, environments, private transcripts, or real test credentials. Keep linked third-party material under its own terms and use synthetic fixtures. See [AGENTS.md](AGENTS.md) for maintenance boundaries and [governance](docs/governance.md) for the configured repository policy.
