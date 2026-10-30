# Maintaining Codex Engineering Skills

This repository maintains reusable engineering instructions, not application frameworks. Choose the smallest sound change; preserve working skill behavior, scope, and installation compatibility.

## Ownership and structure

- `skills/<name>/` is an independently installable package. Keep `SKILL.md`, `agents/openai.yaml`, references, required assets/scripts, and `LICENSE` inside it. No dependency on another skill's relative files.
- Keep maintained developer tooling in Python. Consumer installation/update uses the existing Skills CLI with the version-specific safeguards in `docs/installing-and-updating.md`; do not build a second installer.
- `scripts/` owns shared validation/packaging/release identity; `tests/` owns their regression tests. Reuse these tools before adding helpers.
- `evals/` holds optional evaluation utilities and deliberately defective synthetic fixtures. Do not fix those source fixtures to make checks pass. Evaluate changes in disposable copies.
- `docs/source-manifest.json` is the original migration snapshot, not a generated current-file inventory. Preserve its historical meaning.

## Skill changes

1. Inspect the relevant skill, its callers/references, and neighboring activation descriptions before planning. Do not load every skill for a localized change.
2. Use the supported `skill-creator` workflow when available. Follow the [Agent Skills specification](https://agentskills.io/specification) and the installed Codex host's metadata rules.
3. Use a valid lowercase hyphenated directory/name and precise `description` frontmatter. State when to activate and where responsibility ends. Avoid overlaps with existing specialists.
4. Keep the main workflow concise. Use progressive disclosure for useful detail; link resources explicitly with portable relative paths and correct case. Avoid duplicated instructions or copied documentation libraries.
5. Research consequential/version-sensitive claims using upstream documentation and relevant source/tests. Distinguish guarantees from recommendations, observations, and uncertainty. Record useful source links in the relevant reference.
6. Preserve user/repository authority, read-only scope, existing sound architectures, and proportional verification. Do not make every simple task a research or planning exercise.
7. Add scripts/templates only for a demonstrated repeated need. Document dependencies, safe invocation, cleanup, and meaningful checks. No personal paths, credentials, implicit global writes, or destructive defaults.

## Verification and reporting

Set up the external validator and development dependency as described in `CONTRIBUTING.md`, then use:

```sh
python scripts/validate_skills.py <changed-skill>
python -m unittest discover -s tests -v
```

Use `scripts/release_manifest.py` for committed per-skill identity and exact collection ZIP verification. Explicit Git `vMAJOR.MINOR.PATCH` tags are the collection version authority; never rewrite published tags or regenerate the historical migration snapshot.

Run full collection validation for cross-cutting changes and before publication. Package changed skills into a fresh ignored output directory when resource discovery or packaging changes. Test executable scripts using their native tools when applicable; Python AST validation alone does not prove execution correctness.

For meaningful changes, inspect realistic failure cases and add focused regressions where they improve evidence. Optional model evaluations require explicit execution and suitable isolation; do not run an expensive campaign for a documentation edit. State exactly what executed, failed, or remains unverified. Structural validation does not establish implicit activation, better agent decisions, or production readiness.

Announce substantial tasks before starting. For formal multi-task work, report findings, changes, tests/evidence, pending issues, and PASS/PARTIAL/FAIL/BLOCKED in chat at each completion. Keep coordination proportional and respect user-requested testing depth.

## Public repository hygiene

- Review the complete diff, references, provenance, and licenses. Retain per-skill MIT notices; do not copy third-party implementation without checking its terms and suitability.
- Never commit `.tools/`, `.runs/`, `dist/`, environments, caches, credentials, private application data, or conversation transcripts. Check new fixture data is synthetic.
- Imported `skills/**` and `evals/fixtures/**` retain their original bytes through Git attributes. Avoid mass line-ending or formatting changes. Review executable file modes for any new scripts.
- Update the README catalog and contribution instructions when capabilities or commands change. Keep evidence dated and bounded; do not invent badges or evaluation results.
- Submit source changes through a feature branch and PR; do not bypass rules. Require CI contexts only after actual successful runs. Follow `SECURITY.md`, `docs/governance.md`, and `docs/releases.md` for repository security and publication.
- Source maintenance does not authorize overwriting globally installed skills, changing repository visibility, or modifying unrelated projects.
