# Go, Flutter, and Dart research

Choose the relevant ecosystem; do not load mobile references for a Go service or import JavaScript architecture conventions into either.

## Official knowledge sources

- [Go documentation](https://go.dev/doc/), [module layout](https://go.dev/doc/modules/layout), and [Go code review comments](https://go.dev/wiki/CodeReviewComments): start with the module's `go`/toolchain version and actual runtime/profile evidence. Research ownership, context/cancellation, synchronization, memory, network/database lifetimes and package contracts as the question requires.
- [Flutter documentation](https://docs.flutter.dev/) and [architecture recommendations](https://docs.flutter.dev/app-architecture/recommendations): match SDK/platform targets, widget/resource lifetimes, rendering measurements and integration requirements. The architecture guide explicitly allows adaptation; a reference application's MVVM or state package is not a migration requirement.
- [Dart documentation](https://dart.dev/), [Effective Dart](https://dart.dev/effective-dart), and [pub workspaces](https://dart.dev/tools/pub/workspaces): inspect language/SDK constraints, library privacy, async semantics, packages and generated code. Current workspace syntax may not work on older SDKs.

When researching mobile behavior, check the underlying Android/iOS documentation and plugin implementation/version if the guarantee depends on permissions, background execution, storage, notifications or platform lifecycle. Flutter alone cannot define an OS scheduling guarantee.

## Repository seeds

- [Caddy](https://github.com/caddyserver/caddy): production Go configuration, module registration, network lifecycle and associated tests; a general service need not become a plugin host.
- [PocketBase](https://github.com/pocketbase/pocketbase): a cohesive Go product with its own embedded-data/application constraints. Study concrete behavior and tests instead of treating it as the architecture for every SaaS backend.
- [Flutter samples](https://github.com/flutter/samples): focused executable demonstrations of specific framework/platform concepts. Sample scope, error handling and dependency choices need production-context review.

## Pinned learning examples

[Caddy module registration](https://github.com/caddyserver/caddy/blob/eb04ed52be5e66c467e9e614bd917b8bb4150d1b/modules.go) and [module tests](https://github.com/caddyserver/caddy/blob/eb04ed52be5e66c467e9e614bd917b8bb4150d1b/modules_test.go) were inspected. They make initialization/import side effects and deterministic lookup behavior concrete. Their registry is a solution to Caddy's requirements, not a reason to add registration or global state to another service. The inspected source header identifies Apache-2.0; recheck file/dependency terms before copying.

[Flutter's platform-image example](https://github.com/flutter/samples/blob/21c71902bb2c7da3cce328ba5946cba2f35a660a/platform_channels/lib/src/platform_image_demo.dart) was read. It retains a future and starts work from an interaction; this can inform a lifecycle investigation without treating the demo as complete retry, recovery, accessibility or authorization guidance. Read the real app's callers/state ownership and official FutureBuilder/platform API behavior before applying a change.

Checked commits were dated 2026-10-30 for Caddy and 2026-10-20 for Flutter samples, and both repositories were non-archived at inspection. These are dated provenance observations, not a permanent maintenance guarantee. PocketBase remains a discovery seed here, not an audited recommendation. No upstream tests or native app builds were executed.
