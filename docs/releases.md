# Versions, releases, and recovery

## One collection version

An explicit Git tag `vMAJOR.MINOR.PATCH` is the collection version authority. There is no separate package-manager registry, per-skill version counter, or duplicated `VERSION` file. GitHub release notes describe the corresponding tag; ordinary documentation changes do not require a release.

The versioned public surface comprises skill names and activation responsibilities, self-contained package/resource layout, documented maintainer commands, and the release-manifest schema. Apply [Semantic Versioning](https://semver.org/): incompatible changes require a major increment, compatible additions a minor increment, and compatible corrections a patch increment. Initial `0.x` releases establish the distribution contract while it matures; explain meaningful compatibility changes in their notes as well.

Never move or reuse a published version tag. Correct a release with a new version. No floating `v1` alias is needed for this collection.

## Three complementary identities

| Identity | Purpose |
| --- | --- |
| Collection tag | Human-readable release choice, such as `vX.Y.Z`. |
| Immutable source commit | Exact repository revision behind that tag. |
| Per-skill Git tree SHA and canonical SHA-256 | Determine whether a complete individual package changed, including resources and file modes. |

Skills CLI maintains its own installation tracking. The release manifest describes published source and artifacts; it does not replace, rewrite, or duplicate the CLI's installed lockfile. When the CLI records a 40-character Git tree hash, compare it with `git_tree_sha`. Its clone fallback can record a 64-character source-folder digest using a different algorithm; that is not directly comparable with this manifest's canonical SHA-256. Use the manifest's per-file digests for byte verification across either acquisition path. A local edit may not appear in tracked source hashes: the CLI does not hash installed changes before updating.

The Python content identity is SHA-256 over the sorted file inventory encoded as compact, key-sorted UTF-8 JSON. Each file entry includes relative path, Git mode, byte count, and SHA-256. Timestamps and absolute checkout paths are excluded. See the script's docstring and tests for the schema. Archive hashes can differ after repackaging because ZIP metadata is separate; the package content identity remains stable.

## Inspect committed source without releasing

```sh
python scripts/release_manifest.py --ref HEAD --json-output .runs/current-manifest.json
python scripts/release_manifest.py --ref HEAD --previous EXISTING_COMMIT --json-output .runs/changes.json
```

These commands read Git objects without checkout or application execution. Output files must be new. Use an actual existing ref in place of `EXISTING_COMMIT`. Only an explicitly selected matching version **tag** supplies `collection_version`; `HEAD` or a commit hash produces `null`, even if it points to a tagged commit. A similarly named branch is not a release authority.

The optional `changes` object lists added, changed, and removed skill names. A repository-only documentation change leaves individual skill identities unchanged. `docs/source-manifest.json` remains the historical migration snapshot and must not be regenerated for releases.

## Release gate

Before creating a release:

1. Review the complete PR, contributor evidence, installation guidance, compatibility implications, and licensing/security impact. Preserve user modifications and all intended package resources.
2. Run full validation and the maintained tooling suite. Review negative-path results and skips. Model evaluations are not mandatory for routine tooling/documentation changes.
3. Verify the current install commands in disposable homes when their behavior or supported CLI changes. Record the tested CLI version and its known limitations.
4. Merge through the protected PR workflow. Require hosted checks only after those exact checks have successfully executed. If an external runner restriction persists, do not label hosted CI as passed; document the limitation and defer a release if its verification cannot be justified.
5. Generate fresh packages and verify them against the exact release Git source. Publish only intended artifacts and public-safe evidence.

## Create a release deliberately

The following uses placeholders; choose the next unused version and a clean, reviewed source revision. Do not copy a nonexistent tag into installation instructions as though it were already published.

```sh
git switch main
git pull --ff-only
git status --porcelain
# Stop if tracked or untracked intended source changes remain.
git tag -a vX.Y.Z -m "Codex Engineering Skills vX.Y.Z"
python scripts/validate_skills.py
python -m unittest discover -s tests -v
python scripts/package_skills.py --output-dir dist/vX.Y.Z
python scripts/release_manifest.py --ref vX.Y.Z --package-dir dist/vX.Y.Z --json-output dist/vX.Y.Z/release-manifest.json
```

For subsequent releases, add `--previous vPREVIOUS_VERSION` to the manifest command, replacing that placeholder with the actual previous tag. For the first release, omit `--previous`; its notes should identify the initial 17-skill inventory. The script verifies the exact ZIP member names and bytes against Git, rejects missing/extra/duplicate/unsafe members, and records artifact SHA-256 values. It does not certify executable permissions or native runtime behavior of future bundled scripts; those require their own checks.

Push only the new verified tag:

```sh
git push origin refs/tags/vX.Y.Z
```

Create a **draft** GitHub Release for that existing tag. Attach all 17 ZIPs and `release-manifest.json`; optionally include a standard checksum list. Verify downloaded assets against the manifest and the tag's source commit before publishing the draft. Release immutability is enabled: published assets cannot be replaced and the release tag cannot be moved or deleted while that immutable release exists. [GitHub's release guidance](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) explains draft-first publication.

Release notes should state the source commit, changed skill inventory, tooling/documentation changes, compatible/breaking changes, actual test and installation evidence, known upstream CLI caveats, and remaining platform limits. GitHub Releases is the maintained release history; do not invent a history before the initial release.

## What updates actually follow

Publishing a release does not update installed skills. In tested Skills CLI 1.7.4, a source without a ref follows the repository's default branch; a source installed with `#REF` retains that ref during updates. A tag-pinned install therefore remains on that release. To move to a later release, deliberately re-add the selected skill(s) with the new tag after backup and review.

Do not use `owner/repo@vX.Y.Z` as a tag selector: `@NAME` is a skill selector in this CLI. Use `owner/repo#vX.Y.Z` or a supported `/tree/REF` URL. The installation guide includes tested examples and explicitly identifies `skills check` as mutating in 1.7.4.

## Recover safely

Stop further updates when an operation fails or only partially completes. Inspect each installed directory and its tracking entry; an exit status alone may hide skipped sources. Restore the saved directory and matching tracking files together, or reinstall the affected selected package from the previous known-good immutable commit/tag after preserving local edits.

Do not run removal against an unbacked modified directory as a recovery shortcut. Do not rewrite a published tag or claim a global update is transactional. See [installation and update safeguards](installing-and-updating.md) for exact consumer commands.
