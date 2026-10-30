---
name: repository-structure-engineering
description: Organize files, modules, packages, and dependency boundaries in single-stack or polyglot repositories. Use for file-placement decisions, code extraction, shared packages, monorepo boundaries, or safe restructuring; skip routine implementation that already fits an established structure.
---

# Repository Structure Engineering

Give code clear ownership and predictable dependencies with the smallest useful structure. This skill owns placement, modularity, and structural evolution; it does not prescribe a framework or replace implementation guidance from relevant language, API, database, security, or testing skills.

## Establish the actual decision

Distinguish placing a file, extracting code, creating a package, reviewing boundaries, and moving existing code. For a local placement decision, inspect the relevant feature and nearest comparable implementation; do not map the entire repository. Broader moves warrant a broader dependency and consumer investigation.

Read applicable instructions. Inspect the manifests, lockfiles, versions, source roots, routing conventions, build/test commands, and affected imports needed for this decision. Include runtime discovery and deployment references when location matters. Directory names alone are insufficient evidence of ownership.

Identify the responsibility, owning application or feature, consumers, required runtime, state/resource lifetime, and allowed dependencies. Find existing equivalents before creating another utility or abstraction. For a new project, establish the real deployment units and sharing needs before selecting a modest starting structure.

## Select only relevant detail

Read the reference matching the current uncertainty; do not load the collection for every task.

| Decision | Reference |
| --- | --- |
| Ownership, common folder names, splitting, or sharing | [ownership-and-placement](references/ownership-and-placement.md) |
| TypeScript/JavaScript imports, Node packages or service composition | [javascript-node](references/javascript-node.md) |
| Next.js routing and server/client boundaries; React/Vite organization | [web-frameworks](references/web-frameworks.md) |
| Flutter/Dart libraries, packages, native files and state ownership | [dart-flutter](references/dart-flutter.md) |
| Go package layout, visibility, modules and workspaces | [go](references/go.md) |
| Polyglot repositories, workspace graphs, build/release isolation | [polyglot-workspaces](references/polyglot-workspaces.md) |
| Existing-code moves, non-source files, enforcement and verification | [safe-restructuring](references/safe-restructuring.md) |
| Current upstream rules, version gates or rationale | [sources](references/sources.md) |

Use official documentation matching the installed toolchain when behavior is uncertain or version-sensitive. Separate language/tool requirements from maintainer recommendations and project choices. A new release is not a reason to upgrade the project during organization work.

## Make the smallest sound structural change

- Prefer the existing owner and convention when suitable. Keep feature-specific code close to its consumers; share code when behavior, ownership, dependencies, and evolution are actually shared.
- Compare keeping code in place with a cohesive extraction before adding directories, packages, or deployable services. Feature-first, layer-first, and hybrid layouts are options with different locality costs.
- Define a useful public surface and dependency direction. Follow deliberate cross-feature APIs rather than reaching into private implementation. A shared library should not import its consuming application's implementation.
- Preserve runtime and security boundaries. A folder, alias, package export, or code-owner rule does not authorize an operation or protect a secret. Do not route browser/mobile code through backend-only modules.
- Split by responsibility and change patterns, not a line limit. Retain closely related code when extraction adds navigation and coordination without clarity. Do not extract hypothetical reusable packages or add a global barrel for every directory.

For a simple placement, state the chosen path, owner, and reason briefly, then complete the authorized work. For restructuring, identify affected consumers and invariants before moving files; preserve compatibility and reviewability. Do not expand a local fix into a repository rewrite.

## Verify and report proportionately

Use existing checks appropriate to the changed imports, package surfaces, routes, generation, and deployment paths. A successful editor rename or development build alone may miss packaging and runtime discovery failures. Stop once relevant checks pass unless a failure or unresolved risk justifies more work.

For read-only audits, preserve application code/configuration. If a report is requested, maintain evidence incrementally at an authorized destination. Report concrete maintenance costs, bounded recommendations, and uncertainty; do not create a permanent directory inventory by default.

State what changed, why it belongs there, checks actually run, and meaningful limitations. Do not claim runtime behavior, consumer compatibility, or improved agent performance from Markdown validation alone.
