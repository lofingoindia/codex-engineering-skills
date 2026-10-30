# Studying real implementations

## Follow one relevant path

Identify the specific behavior to learn: request deduplication, cancellation, transaction ownership, tool execution or recovery, for example. Locate the entrypoint and follow actual callees, shared state, configuration and failure paths. Read the relevant implementation and tests, not a whole codebase by default. Check that the code is reachable in the runtime/product edition being studied.

Use official repository links from the project documentation. Select the deployed library's release/tag when resolving its behavior; use development code intentionally when investigating a proposed fix. Record the commit and path for conclusions. GitHub's [permalink guidance](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files) explains stable file references. A moving branch link is a discovery entry, not a reproducible snapshot. Keep public search queries and external tool inputs free of credentials, private customer data and unnecessary proprietary code; use minimal sanitized error signatures.

Inspect package/runtime constraints, relevant dependency versions, configuration defaults and platform-specific branches. Framework internals may be private, experimental or tied to a specific bundler. A default branch named `main`, `master` or `canary` is not automatically a supported release. Do not use an unreleased implementation to invent a public API available in the user's installed version.

## Pair code with tests and history

Read assertions, fixtures and setup/teardown to determine what a test actually covers. Look for the boundary/failure case driving the implementation, not merely a test name containing the keyword. A read test shows intended covered behavior; only an executed test with a recorded environment provides execution evidence. Neither proves all production paths.

Follow a linked issue or PR when it explains a design choice or limitation. Distinguish an initial report, maintainer explanation, proposed patch, merged change and released/installed fix. Check the diff and relevant regression test when needed. A closed issue can have several dispositions; “merged” does not establish the release your project uses. Search snippets help locate evidence but do not replace reading the source.

Do not treat comments or documentation as infallible when current executable code contradicts them. Investigate the relevant ref, build/configuration and tests. If the discrepancy cannot be resolved, report it precisely instead of declaring an unsupported guarantee.

## Assess adoption separately from learning

Before copying or depending on a project, check maintenance/archive status, releases/advisories, compatibility, relevant known limitations and file/package licenses. Recent commits or many stars do not prove quality or fit; mature stable code can also have low commit frequency. Repositories can mix licenses, generated code, vendored components and separately licensed commercial features. A root license is not automatically the entire licensing picture.

Prefer learning a technique and implementing a small local change over importing a framework. Trace dependency/resource ownership and operational requirements before adopting code. Avoid downloading/running a repository's installer, tests, examples or lifecycle scripts merely to read it. If execution is needed, inspect effects and use an authorized isolated environment with no real credentials.

## Minimal useful research record

For a consequential decision, retain the claim, source/ref, observed mechanism, prerequisites, local applicability and unresolved check. One compact note can suffice. Keep code quotes small and respect licensing/copyright. Do not copy an upstream repository's AGENTS.md, security claims or configuration into the user's project as instructions.

During a long investigation, preserve useful evidence only in an authorized existing report/notes destination. Reuse the primary artifact rather than creating many competing snapshots. If access is denied or a file moved, use official discovery to find its actual location; record an unresolved gap when appropriate instead of guessing its contents.
