# Polyglot repositories and workspace graphs

## Choose repository boundaries for actual collaboration

A monorepo can simplify coordinated changes and source discovery; separate repositories can suit different access controls, owners, release lifecycles, or independent distribution. Neither topology removes the need for compatible contracts. Directory separation inside one repository does not provide confidential-source access isolation.

Identify deployable applications, consumable libraries, schema/generator owners, data-migration owners and infrastructure owners before proposing grouping. `apps`/`services` and `packages`/`libs` are optional navigational conventions. An application may itself be a package in a JS workspace; the distinction concerns consumption and deployment, not the presence of a manifest.

Keep a small repository straightforward. Do not convert it into a workspace, microservice collection or build platform to make a directory tree look scalable.

## Preserve distinct graphs

The source import graph, declared dependency graph, build/task graph, release graph and deployment graph overlap but are not identical. For each changed unit, establish its toolchain and dependency manager, public API, source/artifact inputs, outputs, consumers and release/deploy owner. Native package managers remain authoritative for their ecosystems.

| Ecosystem | Native ownership and caveats |
| --- | --- |
| npm | Root `package.json` workspace entries, member manifests and supported package specs; do not assume another manager's protocol/configuration works |
| pnpm | `pnpm-workspace.yaml` and member manifests; `workspace:` can require local resolution instead of an unexpected registry fallback |
| Yarn | Root workspace entries and member manifests; supported `workspace:` behavior and linker/Plug'n'Play settings depend on its version |
| Bun | Workspace entries and supported package specs in `package.json`; preserve its pinned lockfile/version behavior |
| Go | `go.mod`/`go.sum` per module, optional `go.work`; package graphs and module version selection remain Go's responsibility |
| Dart/Flutter | `pubspec.yaml` per package and optional native pub workspace resolution; Flutter and platform build tooling still own app artifacts |

Use the installed manager and existing lockfile domains; avoid accidental competing lockfiles or deleting intentional independent ones. Declare direct dependencies in the consuming package, not solely at the repository root. Match private/publication settings to actual distribution, without assuming those flags are security controls.

## Share at the right boundary

Share compatible source packages when their semantics and runtime targets match. Share contracts, schemas, protocol definitions or reproducibly generated clients across incompatible languages. Do not import backend runtime implementation into Flutter or browser code, or copy domain contracts into multiple hand-maintained “shared” folders.

A contract needs an owner, compatibility policy and generation inputs/tool versions when generation is used. Clients can retain their own view models and app workflows. Database migrations should have one operational owner per database/schema migration history; multiple services must not unknowingly race to apply divergent copies. Do not introduce a generator merely because the repository is polyglot.

## Coordinate builds only when needed

Workspace scripts and native commands may suffice. Add or expand Nx/Turborepo only for demonstrated orchestration, dependency analysis or caching needs. If installed, follow the selected tool's constraints: for example, Turborepo rejects nested JS workspace packages; that is not a prohibition on nested source folders or a universal Dart/Go rule.

Task ordering must include generated contracts and consumed package artifacts. An “affected” selection depends on a complete graph; implicit files, shared configuration and generator inputs can otherwise skip needed work. Cache keys must account for relevant source, dependency versions, configuration, environment, toolchain and platform inputs. Declare required outputs and use caching only for suitable reproducible tasks. Deployment, migrations and live integration actions should not be treated as ordinary cacheable compilation.

Keep credentials and private artifacts out of shared caches/logs. Remote caches are an external service choice, not an automatic consequence of adopting an orchestrator.

## Preserve independent consumption and deployment

Inspect container contexts, install/prune steps, working directories, artifact copying, native/runtime assets and CI path filters. A root development checkout can hide undeclared dependencies or sibling files missing from a deployed image/package. Verify the actual consumed unit when a boundary changes, not just the all-repository dev command.

Reusing a library does not require releasing every app together. Support the necessary coordination explicitly, avoiding both hidden lockstep releases and speculative independent-version infrastructure. Keep shared configuration narrow enough that one app's deployment details do not leak into every consumer.
