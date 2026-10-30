# Dart and Flutter organization

## Preserve the kind of project

Inspect `pubspec.yaml`, SDK constraints, lockfile ownership, analyzer options, generation, assets, native targets, routing, state management and dependency composition. Distinguish a Flutter app, reusable Dart package, Flutter package, plugin, and command-line tool. They have different entrypoints and platform requirements.

A Flutter application's normal entrypoint is `lib/main.dart`, possibly with explicit flavor entrypoints. Do not move it into Dart CLI `bin` to satisfy generic pub package advice. Keep Flutter's native project directories and their Gradle, Xcode, entitlements, identifiers and signing configuration attached to the appropriate app/plugin. Moving Dart source does not justify recreating native projects.

## Libraries and package APIs

Reusable package APIs usually expose selected libraries under `lib`; implementation can live under `lib/src`. Consumers should use intended APIs rather than another package's `src` libraries. This is a convention supported by analyzer rules such as `implementation_imports`, not a runtime access-control wall.

Dart underscore-prefixed identifiers are private to their library, not their package or directory. A Dart file and its declared parts form a library. Splitting a file into separate libraries can therefore change access to private members; moving generated parts can break `part`/`part of` and generator relationships. Do not expose private members or turn unrelated files into parts solely to accommodate a cosmetic split.

Use idiomatic `lowercase_with_underscores` file/directory names and existing import conventions. Keep generated files distinguishable, retain the generator's source of truth and regenerate with the existing command when required. Avoid editing generated serialization, localization or provider/router output directly.

## Ownership within the app

Flutter's architecture guide recommends UI/data separation, views/ViewModels, and repositories/services, while explicitly describing recommendations as adaptable. Use these responsibilities to understand the project; do not force a folder tree, MVVM conversion, state library, or pass-through repository layer.

Feature-first, layer-first and hybrid organization can each fit. Keep a screen's widgets, state/controller and feature models near their owner where that matches the app. Shared widgets should have reusable semantics and theme/accessibility contracts; “used on two screens” does not automatically justify a package.

Separate transport DTOs, persistent records and UI/domain models when their responsibilities differ, rather than sharing every model everywhere. Keep provider/Bloc/ViewModel ownership aligned with screen, session, tenant or application lifetime. Moving composition to a root “providers” directory can accidentally make previously scoped state global; location does not determine lifetime by itself.

Keep app-specific navigation, permissions and integration setup out of general-purpose libraries. Pure Dart packages can be shared where they do not require Flutter/native runtime behavior. A Flutter plugin must preserve its platform implementations and registration/build metadata.

## Workspaces and resources

Use a pub workspace only when coordinating multiple packages provides value. Workspace resolution requires Dart 3.6 or later and compatible SDK constraints on members; workspace globs require Dart 3.11 or later. Verify the pinned SDK rather than applying current syntax to older projects.

A pub workspace shares dependency resolution, a root lockfile and package configuration; it does not allow conflicting versions of the same dependency to coexist freely. Each package still declares its dependencies. Preserve deliberate standalone consumer checks when a workspace could mask compatibility problems.

After relevant moves, verify asset/font declarations and package-qualified asset references, localization inputs, generated imports, test discovery and native paths. Follow existing `test`, `integration_test`, and `tool` conventions. Preserve application lockfiles and the repository's deliberate library/distribution policy; do not clean away native files, generated sources or lockfiles merely because they look infrastructural.
