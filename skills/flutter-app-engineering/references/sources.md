# Authoritative source, version, and tooling register

Researched 2026-10-30. Guidance is original engineering synthesis, not copied manuals or upstream skill recipes. Consult matching SDK/package/native-platform documentation for version-sensitive decisions. Architecture recommendations, API contracts, mobile security standards and platform/store policies have different authority.

## Versions and scope

The official stable branch [Flutter changelog](https://github.com/flutter/flutter/blob/stable/CHANGELOG.md) and [3.47.9 release](https://github.com/flutter/flutter/releases/tag/3.47.9) identified Flutter 3.47.9 as the latest stable hotfix observed. The [Dart stable metadata](https://storage.googleapis.com/dart-archive/channels/stable/release/latest/VERSION), retrieved directly, reported Dart 3.13.7 dated 2026-10-22. [Flutter's archive](https://docs.flutter.dev/install/archive) explains channel/bundled-Dart compatibility. These are dated observations, not permanent pins or instructions to upgrade unrelated projects.

Local read-only version checks reported Flutter 3.47.7 stable with bundled Dart 3.13.5, and standalone `dart --version` also reported 3.13.5. No SDK/channel change was made. Respect project pins and `pubspec` constraints; the newest standalone Dart is not automatically the Dart bundled with a project's Flutter SDK. Use [Flutter release notes](https://docs.flutter.dev/release/release-notes), [Dart changelog](https://dart.dev/changelog), migrations and relevant security advisories when upgrading.

## Official skills and tools: complement rather than duplicate

The [Flutter AI tooling guide](https://docs.flutter.dev/ai/tools), [Flutter agent-plugins](https://github.com/flutter/agent-plugins) and [Dart skills](https://github.com/dart-lang/skills) were inspected, including actual repository paths and selected SKILL.md files. Upstream main-branch skills evolve independently of an installed app/package.

| Upstream workflow | Appropriate use, subject to installed-version and user scope |
| --- | --- |
| [flutter-apply-architecture-best-practices](https://github.com/flutter/agent-plugins/blob/main/skills/flutter-apply-architecture-best-practices/SKILL.md) | Intentional structure/feature architecture work; its example MVVM/layer organization does not require replacing sound existing state management |
| [flutter-setup-declarative-routing](https://github.com/flutter/agent-plugins/blob/main/skills/flutter-setup-declarative-routing/SKILL.md) | Deliberate Router/deep-link/nested-navigation setup, rather than a mandatory migration for a local navigation fix |
| [flutter-build-responsive-layout](https://github.com/flutter/agent-plugins/blob/main/skills/flutter-build-responsive-layout/SKILL.md) | Allocated-space and constraint-based layout work on supported form factors |
| [flutter-use-http-package](https://github.com/flutter/agent-plugins/blob/main/skills/flutter-use-http-package/SKILL.md) | A matching package:http implementation task; reuse an existing suitable client and validate the actual API success/body contract |
| [flutter-add-widget-test](https://github.com/flutter/agent-plugins/blob/main/skills/flutter-add-widget-test/SKILL.md), [flutter-add-integration-test](https://github.com/flutter/agent-plugins/blob/main/skills/flutter-add-integration-test/SKILL.md) | Focused widget or app-interaction tests with supported tooling; test-driver hooks/runtime access require the actual compatible setup |
| [dart-run-static-analysis](https://github.com/dart-lang/skills/blob/main/skills/dart-run-static-analysis/SKILL.md) and the Dart skill catalog | Matching analysis/dependency/unit-test workflows; inspect dry runs and scope instead of applying every mechanical fix or new lint policy across an app |

Read current upstream instructions before invoking a workflow. Examples do not override actual API contracts: a success-status example is not an exhaustive status list; compute sendability is governed by its API; and an infinite animation cannot safely use unconditional pumpAndSettle. Do not fork a competing workflow, copy whole docs, install every plugin, or impose scaffolding on a focused repair.

The Dart/Flutter MCP server offers analyzer/symbol/test/runtime capabilities; Developer Knowledge MCP searches documentation; package skills can supply installed-library workflows. Discover connected tools and prerequisites instead of guessing names or assuming all runtime actions are available. No Dart/Flutter MCP or documentation-search MCP tool was connected in this environment, and no plugin/configuration was installed.

[skills_lint](https://pub.dev/packages/skills_lint) is the upstream Dart skill linter. Its inspected [repository rules](https://github.com/dart-lang/skills/blob/main/repo_tool/skills_lint.yaml) include relative-path and trailing-whitespace checks. No global skills_lint executable/package was found; normal creation checks reuse the bundled Codex validator and local integrity checks. They do not claim execution of the Dart linter or app tests.

## Framework, state, data and rendering contracts

| Primary sources | Retained engineering judgment |
| --- | --- |
| [Architecture guide](https://docs.flutter.dev/app-architecture/guide), [recommendations](https://docs.flutter.dev/app-architecture/recommendations), [Effective Dart](https://dart.dev/effective-dart/usage) | Clear UI/data ownership and idiomatic Dart; MVVM/repositories and optional domain layers are adaptable recommendations |
| [State lifecycle](https://api.flutter.dev/flutter/widgets/State-class.html), [setState](https://api.flutter.dev/flutter/widgets/State/setState.html), [dispose](https://api.flutter.dev/flutter/widgets/State/dispose.html), [context mounted](https://api.flutter.dev/flutter/widgets/BuildContext/mounted.html), [FutureBuilder](https://api.flutter.dev/flutter/widgets/FutureBuilder-class.html) | Identity versus rebuild, async UI validity and Future ownership; cleanup and freshness are separate guarantees |
| [Future timeout](https://api.dart.dev/dart-async/Future/timeout.html), [Future wait](https://api.dart.dev/dart-async/Future/wait.html), [subscription cancel](https://api.dart.dev/dart-async/StreamSubscription/cancel.html) | Stop-waiting versus cancellation, sibling outcomes and asynchronous cleanup |
| [Provider](https://pub.dev/packages/provider), [Riverpod disposal](https://riverpod.dev/docs/concepts2/auto_dispose), [flutter_bloc](https://pub.dev/packages/flutter_bloc) | Created versus borrowed state, listener/auto-dispose lifetimes and matching update scope; no default library migration |
| [Flutter networking](https://docs.flutter.dev/cookbook/networking/fetch-data), [http](https://pub.dev/packages/http), [AbortableRequest](https://pub.dev/documentation/http/latest/http/AbortableRequest-class.html), [Dio](https://pub.dev/packages/dio) | Reuse owners and inspect installed cancellation/interceptor/error semantics instead of duplicating clients |
| [Offline-first options](https://docs.flutter.dev/app-architecture/design-patterns/offline-first), [package dependencies](https://dart.dev/tools/pub/dependencies) | Product-specific offline guarantees, authoritative repositories/state, durable replay and reproducible compatible app dependencies |
| [Navigation](https://docs.flutter.dev/ui/navigation), [deep linking](https://docs.flutter.dev/ui/navigation/deep-linking), [go_router](https://pub.dev/packages/go_router) | Simple versus advanced routing, built-in/plugin integration and deliberate retained branch state |
| [Adaptive UI](https://docs.flutter.dev/ui/adaptive-responsive), [accessibility](https://docs.flutter.dev/ui/accessibility), [internationalization](https://docs.flutter.dev/ui/internationalization) | Constraints/insets, supported form factors, semantics, assistive technology and locale-correct content |
| [Performance practices](https://docs.flutter.dev/perf/best-practices), [profiling](https://docs.flutter.dev/perf/ui-performance), [memory tools](https://docs.flutter.dev/tools/devtools/memory), [Impeller](https://docs.flutter.dev/perf/impeller), [isolates](https://docs.flutter.dev/perf/isolates), [compute](https://api.flutter.dev/flutter/foundation/compute.html) | Diagnose build/layout/raster/native costs, real-device evidence, engine/platform differences and CPU offloading tradeoffs |

## Native behavior, security and production evidence

| Primary sources | Retained engineering judgment |
| --- | --- |
| [AppLifecycleState](https://api.flutter.dev/flutter/dart-ui/AppLifecycleState.html), [AppLifecycleListener](https://api.flutter.dev/flutter/widgets/AppLifecycleListener-class.html) | Flutter/native states differ; notifications are not guaranteed before termination |
| [Android task scheduling](https://developer.android.com/develop/background-work/background-tasks/persistent), [Apple Background Tasks](https://developer.apple.com/documentation/backgroundtasks), [Apple background strategies](https://developer.apple.com/documentation/backgroundtasks/choosing-background-strategies-for-your-app) | Supported scheduled/continued work, transfers and finite OS budgets rather than indefinite Dart execution. Apple Markdown versions were fetched for the actual article content |
| [Android permissions](https://developer.android.com/training/permissions/requesting), [Keystore](https://developer.android.com/privacy-and-security/keystore), [Apple Keychain](https://developer.apple.com/documentation/security/keychain-services) | Contextual permission UX and platform-backed key/credential storage with deployment/access-policy limits |
| [FCM Flutter receipt](https://firebase.google.com/docs/cloud-messaging/flutter/receive-messages), [token management](https://firebase.google.com/docs/cloud-messaging/manage-tokens) | Bounded handlers, entry-point/platform differences, navigation intents, device-token ownership and non-guaranteed delivery |
| [OWASP MASVS](https://mas.owasp.org/MASVS/), [MASTG](https://mas.owasp.org/MASTG/), [native OAuth BCP](https://www.rfc-editor.org/rfc/rfc8252.html), [OAuth security BCP](https://www.rfc-editor.org/rfc/rfc9700.html) | Risk-appropriate storage/privacy/auth boundaries; public native clients, external user-agents and PKCE rather than embedded secrets |
| [Testing overview](https://docs.flutter.dev/testing/overview), [integration tests](https://docs.flutter.dev/testing/integration-tests), [pumpAndSettle](https://api.flutter.dev/flutter/flutter_test/WidgetTester/pumpAndSettle.html), [error handling](https://docs.flutter.dev/testing/errors) | Match evidence to the actual boundary; deterministic async checks, native-test limitations and distinct error coverage |
| [Android release](https://docs.flutter.dev/deployment/android), [iOS release](https://docs.flutter.dev/deployment/ios) | Existing signing/flavors/identity, platform toolchains, symbols and real release compatibility; macOS/Xcode required for iOS builds |

## Skill authoring and verification limits

The bundled `skill-creator/SKILL.md`, UI metadata guide, initializer and validator were inspected. [OpenAI Astra guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), the [Skills guide](https://developers.openai.com/api/docs/guides/tools-skills), [Agent Skills specification](https://agentskills.io/specification), and [evaluation guidance](https://developers.openai.com/blog/eval-skills) were researched in this conversation and inform precise activation, progressive disclosure and truthful proportional verification.

This installation uses normal structural/metadata/link/whitespace/package checks as requested. No agent evaluations, activation trials, baseline comparisons, Flutter application fixtures, device tests or benchmark campaigns ran. Future application work should obtain relevant interaction evidence; static skill validation does not prove improved agent decisions or production app quality.
