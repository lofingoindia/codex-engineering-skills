# Research and upstream rules

Research checked **2026-10-30**. Use this register to resolve a specific structural uncertainty, not as a reading list to load in full. Consult documentation matching the project's installed version before applying configuration examples. No source establishes one universal repository tree.

## How to interpret the guidance

Language visibility, module resolution, routing discovery and tool configuration have enforceable behavior. Maintainer layout examples and architectural recommendations express design choices. The ownership/extraction decision framework in this skill is an engineering synthesis of those constraints, not a normative folder standard.

At research time, live pages displayed Node documentation v26.13.0, Next.js v16.4.3, Nx v24, npm v12.2.1, and a Dart language-documentation baseline of 3.13.3. These are source context, not mandatory upgrades or an assertion about every installed SDK. Version-sensitive details should be rechecked when used. In particular, Dart pub workspaces require 3.6+, and workspace globs require 3.11+.

## Skill design and discovery

- [Agent Skills specification](https://agentskills.io/specification): required metadata, naming and progressive disclosure. The open format is distinct from product-specific UI metadata.
- [Codex skills](https://developers.openai.com/codex/skills/): invocation/discovery and user-level skill placement; use the active environment's supported skill directory.
- [OpenAI skills guide](https://developers.openai.com/api/docs/guides/tools-skills): manifests, supporting resources and skill routing; API upload mechanics are not required for a local Codex skill.
- [GPT-6 Astra skill/prompt guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra): narrow descriptions, conditional references and outcome-focused guidance without oversized itineraries.
- [Skill evaluation guidance](https://developers.openai.com/blog/eval-skills): distinguishes instruction validity from demonstrated behavioral performance. Reading it does not constitute executing evaluations.

The installed skill-creator instructions and `references/openai_yaml.md` were also inspected. This package uses their normal initializer/validator workflow and default implicit invocation; it does not depend on another engineering skill being installed.

## JavaScript, TypeScript, and Node.js

- [TypeScript modules reference](https://www.typescriptlang.org/docs/handbook/modules/reference.html): consumer-specific resolution, `paths` not rewriting emitted code, and why aliases into workspace-package source bypass package semantics.
- [TypeScript project references](https://www.typescriptlang.org/docs/handbook/project-references.html): optional compilation partitioning, composite/declaration requirements and `tsc -b` build ordering. References do not replace package-manager dependencies.
- [Node package rules](https://nodejs.org/api/packages.html): package `type`, entrypoints, subpaths and conditional exports; restricting exports has compatibility consequences and is not strong isolation.
- [Node ESM](https://nodejs.org/api/esm.html): native specifier/extension rules and URL-based module identity; do not assume bundler resolution also works in Node.

## Next.js, React, and Vite

- [Next.js project organization](https://nextjs.org/docs/app/getting-started/project-structure): App Router entry files, colocation, optional private folders, route groups and optional `src`.
- [Next.js layouts/pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages): routing composition and layout ownership; location can affect navigation/state behavior.
- [Next.js server/client components](https://nextjs.org/docs/app/getting-started/server-and-client-components): client import boundaries, composition and server-only environment protection. Folder names alone do not enforce these rules.
- [Pages Router pages/layouts](https://nextjs.org/docs/pages/building-your-application/routing/pages-and-layouts): distinct filesystem-route conventions; do not apply App Router colocation assumptions blindly.
- [Package transpilation](https://nextjs.org/docs/app/api-reference/config/next-config-js/transpilePackages) and [deployment output/tracing](https://nextjs.org/docs/app/api-reference/config/next-config-js/output): consumer compilation and deployment artifact inclusion are separate concerns. Current behavior varies with router and bundler.
- [React state ownership](https://react.dev/learn/sharing-state-between-components) and [custom hooks](https://react.dev/learn/reusing-logic-with-custom-hooks): composition and shared logic versus shared state; neither prescribes a folder layout.
- [Vite linked dependencies](https://vite.dev/guide/dep-pre-bundling) and [Vite features](https://vite.dev/guide/features): source treatment of linked packages, development optimization and path-based module discovery. Avoid treating development success as deployment proof.

## Dart and Flutter

- [Dart package layout](https://dart.dev/tools/pub/package-layout): public libraries, implementation convention, tests/tools and package resources. Flutter app entrypoints follow Flutter conventions.
- [Dart libraries/privacy](https://dart.dev/language/libraries): library-based underscore privacy and parts; directory or package ownership is a different boundary.
- [Implementation-import lint](https://dart.dev/tools/linter-rules/implementation_imports): analyzer support for avoiding another package's `lib/src` implementation.
- [Effective Dart style](https://dart.dev/effective-dart/style): idiomatic names; preserve the language's conventions rather than importing JS naming rules.
- [Pub workspaces](https://dart.dev/tools/pub/workspaces): SDK gates, member declarations, shared resolution/lockfile/package configuration and dependency conflicts.
- [Flutter architecture guide](https://docs.flutter.dev/app-architecture/guide) and [recommendations](https://docs.flutter.dev/app-architecture/recommendations): recommended responsibilities and conditional architectural choices. They explicitly allow adaptation; they do not justify forced MVVM/state-management rewrites.

## Go

- [Go module layout](https://go.dev/doc/modules/layout): simple roots, multiple packages, commands and internal implementation. Examples are guidance, not a required enterprise tree.
- [Go command visibility rules](https://pkg.go.dev/cmd/go#hdr-Internal_packages): actual `internal` import-prefix restriction; repository membership alone is insufficient.
- [Go package names](https://go.dev/blog/package-names): meaningful cohesive APIs and costs of generic `util`/`common` collections; older design guidance whose relevant principles remain applicable.
- [Go module/workspace reference](https://go.dev/ref/mod#workspaces) and [workspace tutorial](https://go.dev/doc/tutorial/workspaces): module dependencies, local multi-module development and caveats about committed workspaces masking consumer versions.

## Workspaces, builds, and enforcement

- [npm workspaces](https://docs.npmjs.com/cli/v12/using-npm/workspaces/), [pnpm workspaces](https://pnpm.io/workspaces), [Yarn workspaces](https://yarnpkg.com/features/workspaces), and [Bun workspaces](https://bun.sh/docs/pm/workspaces): each manager's actual declaration/linking/package-spec behavior. Similar names do not establish interchangeable configuration or protocol support.
- [Turborepo structure](https://turborepo.dev/docs/crafting-your-repository/structuring-a-repository): optional apps/packages convention and tool-specific nesting constraints, not a cross-language standard.
- [Turborepo caching](https://turborepo.dev/docs/crafting-your-repository/caching): deterministic tasks, inputs, outputs and cache correctness; adopting a task runner does not require remote caching.
- [Nx module boundaries](https://nx.dev/docs/features/enforce-module-boundaries): JS import linting versus broader project-graph enforcement and their feature/licensing scope. Reuse only appropriate installed capabilities.
- [ESLint restricted imports](https://eslint.org/docs/latest/rules/no-restricted-imports): a built-in static-import restriction; not complete coverage of runtime discovery or security.
- [GitHub code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners): review ownership and path-sensitive configuration, not source confidentiality or authorization.
- [Git move command](https://git-scm.com/docs/git-mv): move/index behavior; a successful rename alone proves neither consumer compatibility nor application correctness.
