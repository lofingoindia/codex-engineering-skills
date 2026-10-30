# Repository governance

This collection uses a small maintainer-led PR workflow. These settings were inspected through the authenticated GitHub interface and verified through GitHub's API during the distribution evolution. Settings can change; verify the live rules when maintaining them.

## Repository and contributions

- Public repository, default branch `main`, MIT-licensed original content.
- Issues and pull requests are enabled. Discussions remain disabled until a distinct community need emerges. Existing description and documentation remain the primary entry points; relevant engineering/technology topics improve discovery.
- Squash merging is enabled; merge-commit and rebase merging are disabled. Merged head branches are deleted automatically.
- The repository currently has one administrator and no additional authorized reviewers. PRs are required, with **zero required approvals**, so the owner can review and merge their own work. There is no mandatory CODEOWNERS review or additional approval bureaucracy.

## Effective branch and tag rules

| Rule | Configuration |
| --- | --- |
| `main-contribution-protection` | Active on the default branch; block deletion and force pushes; require a PR and resolution of review conversations; allow squash merge; zero required approvals. |
| `immutable-version-tags` | Active on `refs/tags/v*`; restrict updates and deletions. New version tags can be created by authorized writers. |
| Bypass actors | None configured. Normal work must follow the protected workflow. |
| Immutable releases | Enabled for future published releases; draft assets must be complete before publication. |

Required CI checks are staged: they must not be configured until the exact checks have actually succeeded and GitHub exposes them. The completion evidence records whether runner availability permitted that step. Do not add an unavailable check or a required independent approval that locks out the solo maintainer. Do not bypass protections or force-push to finish routine work.

Rule configuration/effective matching and the actual PR merge provide verification. No destructive force-push, branch deletion, or published-tag rewrite is required to test these protections.

## Security and automation

- Dependabot alerts, dependency graph, and security updates are enabled. Monthly version-update PRs cover Python development requirements and pinned GitHub Actions; security updates are handled separately by Dependabot.
- Secret scanning and push protection are enabled. Private vulnerability reporting is enabled; use [SECURITY.md](../SECURITY.md).
- The default Actions token is read-only and cannot approve pull requests. Workflows explicitly request only `contents: read`.
- Actions are restricted to GitHub-owned actions and full commit pins. The external OpenAI validator is a reviewed, pinned checkout, not an unpinned remote script or vendored dependency.
- Workflows from all external contributors require maintainer approval. Public-fork testing uses `pull_request`, without secrets or privileged `pull_request_target` execution. Approve only after examining changed workflow/tool code; checks still execute contributor code.
- CI cancels superseded runs and uses a single validation workflow. Optional model evaluations are excluded. The workflow covers Windows, Ubuntu, and macOS with Python 3.13 and verifies package content against committed Git source.

CodeQL/AI scanning and automatic AI fixes were not enabled as a blanket default. The repository contains intentionally vulnerable evaluation fixtures, and a useful future code-scanning setup should scope those appropriately rather than create noisy alerts or consume credits without a clear need. Review and focused regressions remain required.

## Maintaining settings

Use the real GitHub interface to inspect changes and API/CLI verification where useful. After saving, verify effective settings rather than treating form submission as success. Repository protections do not authorize account billing changes, wider token permissions, or modifications to installed user skills.

Keep new controls proportional. A new maintainer, workflow, third-party action, or reviewer requirement may justify revisiting this policy. Record actual changes and remaining limits in completion evidence; do not claim that configuration proves all attacks are prevented.
