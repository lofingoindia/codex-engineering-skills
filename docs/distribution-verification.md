# Public distribution evolution: verification record

Local verification date: **30 October 2026**. Baseline source: `35669c283e8e98cacc702295dea6d1b7a4bad6b8`. This record covers the subsequent tooling/distribution work; the earlier [consolidation evidence](verification.md) remains historical.

## Executed local evidence

| Area | Actual result |
| --- | --- |
| Rechecked baseline | All 17 skills validated; all original 24 tooling tests passed before changes. |
| Maintained Python tools | **48 tests passed** on Windows/Python 3.13.17, preserving all original tests. Added coverage for name selection outside the checkout, unsafe report/resource paths, Windows junctions, changed-source packaging, cleanup, Git identities, ref failures, and corrupt/mismatched ZIPs. |
| Skill preservation | All 17 skill packages retain their original guidance and resources. No skill or evaluation-fixture rewrite was part of this evolution. |
| Packaging | All **17 ZIP packages / 150 source files** validated and matched committed source through release-manifest verification. Release assets are verified again against their exact final tag before publication. |
| Skills CLI | Published **1.7.4**, npm gitHead `a80e4c9d12d607631249d4d7d059f835d4b2f13a`, tested with Node 24.22.1; requires Node >=22.20. |
| Isolated distribution checks | **29 focused assertions passed**: public discovery, one/all/project installs, full file equality, selected/multiple/all updates, retained commit ref, local changes, missing metadata, conflicts, removal, Windows links, download failures, interruptions, and recovery. |
| Real user installations | The CLI investigation compared **184 existing installed files before/after**, with no change; the existing canonical `.agents/skills` user directory was not created or modified. All mutating CLI tests used disposable homes/state/cache directories. |
| Optional agent evaluations | Existing runner and fixtures retained. Preparation remains distinct from execution; no model calls or agent-quality comparison campaign ran. |

The source-hash mismatch needed to trigger some update paths was simulated only in disposable tracking metadata. The released CLI then performed real source acquisition/reinstallation. This does not prove arbitrary interruption safety or transactional updates across a collection.

## Upstream capability limits found

The published CLI dispatches `check` to its update implementation. Actual sandbox checks confirmed it can replace files; unsupported `--dry-run` and `--check` flags do not prevent this. Recent stable versions inspected had the same issue. Upstream `main` contains unreleased differences, so the published package was tested and cited separately.

The CLI does not detect/protect installed local edits, retain all copy/agent choices during update, repair every missing tracked directory, or make multi-skill updates atomic. These are documented in [installation and update safeguards](installing-and-updating.md), with backup/candidate comparison and explicit selected-source re-add. Read-only source/release/manifest comparison is available; a safe built-in `skills check` is not claimed for 1.7.4.

The subsequent `v0.1.0` candidate-tag installation copied all 17 packages/150 files correctly and retained the selected ref. The GitHub tree API was unavailable for that acquisition, so the CLI recorded 64-character fallback folder hashes. An initial direct comparison with Git tree SHAs was an invalid oracle; byte comparison still passed. Upstream source established the two formats, and the installation/release guidance was corrected. The immutable candidate tag was preserved; the documentation correction advances the candidate patch version rather than rewriting history.

## GitHub configuration evidence

Authenticated interface inspection and saved-setting/API readback established:

- Public repository and `main` default branch; one administrator, no other authorized reviewers.
- Squash-only merges and automatic merged-branch deletion.
- Active `main-contribution-protection` ruleset: PR required, zero approvals, review conversations resolved, force pushes and deletion blocked, no bypass list.
- Active `immutable-version-tags` ruleset: `refs/tags/v*` updates/deletions restricted, without blocking authorized new tags.
- Immutable releases enabled; private vulnerability reporting, dependency graph/Dependabot alerts/security updates, secret scanning, and push protection enabled.
- Actions default token read-only; PR approval permission disabled; GitHub-owned actions only with full-SHA pin enforcement; all external contributors require workflow approval.

General release/merge controls and vulnerability reporting/alerts were configured in the UI. API calls complemented the UI for precise rules/policy/security fields, and the saved rules/security pages were inspected. No billing settings, account credentials, repository visibility, or real global skills were changed. Protection was verified through effective rules and the contribution workflow rather than destructive force/deletion probes.

Monthly Dependabot updates, a PR template, two issue forms, and a private security-report link are included. CodeQL/AI scanning was not added indiscriminately to deliberately defective fixtures. See [governance](governance.md) and [SECURITY.md](../SECURITY.md).

## Hosted CI and release evidence

The validation workflow now configures Windows, Ubuntu, and macOS/Python 3.13 and verifies collection archives against Git source. Local Windows success is not a claim that those hosted jobs ran. On non-Windows hosts, one native Windows-junction test is expected to skip; the portable resource-escape test still runs.

The historical consolidation workflow failed before job startup under an account restriction. The public PR/current commit's [Actions results](https://github.com/lofingoindia/codex-engineering-skills/actions) and published release notes are the authoritative subsequent execution record. Required status checks must be added only after those exact contexts succeed; any external runner restriction must be reported rather than bypassed or labeled a pass.

Release publication uses an existing immutable source/tag, fresh verified archives, and the generated content manifest. A release is not claimed merely because the script can prepare metadata. Inspect [GitHub Releases](https://github.com/lofingoindia/codex-engineering-skills/releases) for actual published tags, commits, assets, and notes. A post-publication tag installation is checked in a disposable home when the initial release is created.

## Limits and reproducibility

Raw commands, logs, dependency caches, and disposable installations remain ignored in `.runs/`, `.tools/`, and `dist/`. They are not published because they can contain personal paths or local context. Maintainer checks are reproducible through [CONTRIBUTING.md](../CONTRIBUTING.md); the normal consumer path needs no Python.

The isolated Skills CLI behavior checks ran on Windows; equivalent macOS/Linux CLI executions are not claimed. Python's hosted matrix is a separate scope. Structural checks do not prove skill activation quality, application correctness, runtime permissions of future scripts, or absence of all sensitive/licensed content. No new installer, registry, daemon, model-evaluation framework, or independent skill-version counters were added.
