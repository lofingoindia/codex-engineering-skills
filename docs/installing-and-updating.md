# Installing and updating

Use the [Skills CLI](https://github.com/vercel-labs/skills) to install complete, independent skill directories from this public repository. Consumers need **Node.js 22.20 or later**, with npm/npx; Git supports the CLI's clone fallback. Python is needed only for the repository's [maintainer tools](../CONTRIBUTING.md), not for installing or using skills. Public installation needs no GitHub account or token.

Commands below pin **`skills@1.7.4`**, the published version checked on 2026-10-30. `npx --yes` allows npm to download that CLI; the final `--yes` skips its installation confirmation. Examples use PowerShell/POSIX-compatible shell syntax; platform verification is bounded below.

> **Before replacing an existing skill:** back up and compare it as described under [Review updates](#review-updates). `add --yes` can overwrite a directory with the same name, including a manually installed or locally modified one. In CLI 1.7.4, **`check` also performs updates**. Neither `check --dry-run` nor `update --check` is a safe alternative: those unsupported flags are ignored. See [the published command dispatch](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/cli.ts#L420-L424) and [option parser](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/update.ts#L66-L85).

## Install for Codex

First browse the available names without installing:

```sh
npx --yes skills@1.7.4 add lofingoindia/codex-engineering-skills --list
```

For a fresh installation, confirm that the selected names do not already exist in your supported skill directories. Install one skill globally:

```sh
npx --yes skills@1.7.4 add lofingoindia/codex-engineering-skills --skill go-backend-engineering -a codex -g --copy --yes
```

Select multiple names after `--skill`, or install all 17 skills with `'*'`:

```sh
npx --yes skills@1.7.4 add lofingoindia/codex-engineering-skills --skill go-backend-engineering nodejs-backend-engineering -a codex -g --copy --yes
npx --yes skills@1.7.4 add lofingoindia/codex-engineering-skills --skill '*' -a codex -g --copy --yes
```

`-a codex` selects Codex, `-g` selects user scope, and `--copy` requests materialized files. Use `--skill '*'` for the whole collection; **`--all` also selects all agents**.

The tested CLI installs global Codex skills at **`~/.agents/skills/<name>/`**. Its `CODEX_HOME` setting affects detection, not that destination. The [published agent configuration](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/agents.ts#L224-L232) defines this path. See [Existing manual installations](#existing-manual-installations) if your host uses `~/.codex/skills`.

For one project, run the command in that project's root and **omit `-g`**:

```sh
npx --yes skills@1.7.4 add lofingoindia/codex-engineering-skills --skill go-backend-engineering -a codex --copy --yes
```

This creates `.agents/skills/go-backend-engineering/` and a project `skills-lock.json`. Decide with the project's maintainers whether to commit them. Refresh discovery as required by your Codex host.

List installed global skills, or list project skills from the project root:

```sh
npx --yes skills@1.7.4 list -g -a codex
npx --yes skills@1.7.4 list -a codex
```

## Review updates

CLI 1.7.4 has **no supported read-only update check or local modification safeguard**. The recent stable versions and snapshot inspected during verification have the same `check` alias; this guide does not recommend downgrading to obtain a safe check. Current upstream `main` contains unreleased changes, so its documentation may describe behavior absent from the published package.

Use this procedure before any `add` or `update` that could replace an existing name:

1. Identify the installation scope, selected directories, and original source/ref. Inspect both the CLI destination and any older manual installation. A matching name does not establish matching content or ownership.
2. Back up each complete selected skill directory and the applicable lock file outside the installation directory. Global CLI metadata normally lives in `~/.agents/.skill-lock.json`; if `XDG_STATE_HOME` is set, it lives at `$XDG_STATE_HOME/skills/.skill-lock.json`. Project metadata is `skills-lock.json` in the project root. Preserve that backup until the replacement is verified.
3. Open a **new, empty review directory** and install the proposed source there using the project command above, without `-g`. Use the same selected names and intended ref. Compare that directory's `.agents/skills/<name>/` with your installed copy, including references, assets, scripts, and license files. For example, replace the first path below with the installed directory:

   ```sh
   git diff --no-index -- "<installed-skill-directory>" ".agents/skills/go-backend-engineering"
   ```

   Git exits 1 when this diff finds differences. A two-way diff shows differences; distinguishing your edits from upstream edits requires the previous source baseline. Keep local changes in a maintained fork or saved copy and resolve them deliberately before replacement.
4. After reviewing the differences, explicitly re-add the selected source and names with `-a codex -g --copy --yes`. The single, multiple, and whole-collection commands above also serve as scoped replacements. Use the project form for project installations.
5. Inspect the resulting files and lock, then refresh discovery. If replacement fails, inspect the selected directories before retrying; restore the backed-up directories and matching lock when recovery requires the previous state.

The CLI compares its **recorded source hash** with upstream, not the installed files with their original content. Local changes may remain unnoticed when upstream is unchanged and be deleted when an update occurs. Reinstallation removes and recreates the destination before copying. See [source-hash comparison](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/update.ts#L596-L604) and [destination replacement](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/installer.ts#L371-L380).

### Built-in update commands

After the same backup and review, these tested upstream commands select **installed skill names**:

```sh
npx --yes skills@1.7.4 update go-backend-engineering -g -y
npx --yes skills@1.7.4 update go-backend-engineering nodejs-backend-engineering -g -y
npx --yes skills@1.7.4 update -g -y
```

The last command considers **all globally tracked sources**, including other collections. `update owner/repo` does not select a repository; it treats that text as a skill name. Unknown names can return no matches with exit 0.

`update` supports scope flags `-g`/`-p`, `-y`, and positional names. It has **no supported `--agent` or `--copy` option**: it detects agents again and can change a previous copy to a link for another agent. Supplying `-a codex` does not constrain it; `codex` is parsed as another skill name. Prefer explicit re-add when Codex scope and copied files must be retained. The [published update child command](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/update.ts#L720-L735) shows the options passed through.

Updates are per skill, not atomic across a collection. Interruption can leave some skills updated and others unchanged. A source-check failure can also be logged while the overall process exits 0. Review output and resulting content; exit status alone does not establish that every selected source was checked. In 1.7.4, a current lock may report a missing installed directory as up to date; explicit re-add can repair it after reviewing any name conflicts.

## Choose a ref or release

An unpinned source follows the repository's default branch. Pin a branch, tag, or full commit with **`#REF`**, quoted for shell portability. This exact public commit was exercised during verification:

```sh
npx --yes skills@1.7.4 add "lofingoindia/codex-engineering-skills#35669c283e8e98cacc702295dea6d1b7a4bad6b8" --skill go-backend-engineering -a codex -g --copy --yes
```

A full GitHub tree URL also selects the ref and skill directory:

```sh
npx --yes skills@1.7.4 add https://github.com/lofingoindia/codex-engineering-skills/tree/35669c283e8e98cacc702295dea6d1b7a4bad6b8/skills/go-backend-engineering -a codex -g --copy --yes
```

For a published release, replace the ref with an existing tag, for example `"lofingoindia/codex-engineering-skills#vX.Y.Z"`. `vX.Y.Z` is a placeholder, not an available release. **`owner/repo@NAME` selects a skill; it does not pin a tag.** The [source parser](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/source-parser.ts#L284-L309) handles refs separately from [the skill selector](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/source-parser.ts#L528-L538).

The lock records the selected `ref`, and built-in update **retains it**. It does not advance a version tag to the next release. To adopt another release, run explicit re-add with its ref after review and backup. Re-adding an older full commit provides the same deliberate rollback path. Full commits identify fixed content; a branch or movable tag can resolve to different content later. See [ref-preserving update source construction](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/update-source.ts#L115-L133).

### Read-only discovery and comparison

Inspect [published releases](https://github.com/lofingoindia/codex-engineering-skills/releases) and [tags](https://github.com/lofingoindia/codex-engineering-skills/tags), or query the remote without changing installed skills:

```sh
git ls-remote https://github.com/lofingoindia/codex-engineering-skills.git HEAD 'refs/tags/*'
npx --yes skills@1.7.4 add lofingoindia/codex-engineering-skills --list
```

A new HEAD or tag does not prove a selected skill changed; `--list` is discovery, not a content update check. When a release provides a content manifest, its `source_commit` identifies the source revision. Compare each selected skill's `content_sha256` between the old and proposed release manifests for upstream changes, then compare installed file bytes with the proposed manifest's per-file `sha256` values for local differences. When GitHub's tree API succeeds, the CLI's global `skillFolderHash` is a 40-character source Git tree SHA, comparable to the manifest's `git_tree_sha`. Clone fallback can instead record a 64-character source-folder SHA-256; do not compare that value with the tree SHA or assume it uses this manifest's canonical hash algorithm. Neither format verifies current installed edits. Compare per-file bytes/digests when formats differ. Project `computedHash` is also a different format. The [released add fallback](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/add.ts#L2255-L2258) and [update hash selection](https://github.com/vercel-labs/skills/blob/a80e4c9d12d607631249d4d7d059f835d4b2f13a/src/update.ts#L648-L652) distinguish these paths.

## Existing manual installations

Older installers and manually copied skills may use `~/.codex/skills`, while this CLI targets `~/.agents/skills`. Check your host's supported discovery paths and avoid duplicate copies of the same name. These commands **do not migrate or update the old directory automatically**.

A directory without Skills CLI lock metadata is ignored by `update`. Missing hash/path metadata can also prevent automatic updates. Explicit `add` may adopt a same-name destination by replacing it, even if it came from a different source. Complete the backup and comparison procedure first; keep the old copy until the intended installation is verified, then remove any obsolete duplicate deliberately.

## Remove skills

Back up local edits first. Remove one globally installed skill from the Codex target:

```sh
npx --yes skills@1.7.4 remove go-backend-engineering -g -a codex -y
```

Remove the skills tracked under this exact repository source:

```sh
npx --yes skills@1.7.4 remove lofingoindia/codex-engineering-skills -g -a codex -y
```

For project scope, run from that project and omit `-g`. Removal updates CLI tracking; it does not clean up an older separate manual installation. Codex shares the canonical `.agents/skills` location with other universal agents, so deleting a directory there removes that shared copy too.

## Verification scope

On 2026-10-30, **29 focused assertions passed** against the published CLI on Windows with Node 24.22.1. Checks covered public discovery; single and 17-skill installation; all 150 skill files matching source bytes; project scope; selected updates; commit-ref retention; local edits and missing metadata; conflicts; removal; Windows junctions; failed or truncated downloads; partial updates; and retry recovery. Real installed skills remained unchanged. No model calls or agent-quality evaluations ran. macOS/Linux execution was not performed; the commands use portable shell syntax, but that does not establish platform behavior. Raw logs and disposable test state remain in ignored local evidence directories and are not distributed.
