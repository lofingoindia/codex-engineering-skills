# Go package, module, and workspace boundaries

## Start with packages, not a foreign directory template

Inspect module paths, `go`/toolchain directives, imports, commands, build tags, embedded files, generated code, `go.work` and replacements. A directory of Go source normally forms a package; several cohesive files can share its unexported implementation. Moving a file into a subdirectory creates a package boundary, not just a visual grouping.

Use short, meaningful package names that make sense at call sites. Avoid introducing generic `util`, `common`, `types` or `interfaces` packages that collect unrelated responsibilities and dependencies. Do not mass-rename sound existing packages during a local task.

Simple packages and commands can live at the module root. `cmd/<command>` is useful for multiple executables or an established service layout, not mandatory for a small program. `main` packages assemble and run commands; shared implementation belongs in importable packages when there is a real reuse boundary. A universal `pkg` directory is not an official requirement or visibility mechanism.

## Visibility and direction

An `internal` directory has a Go-tool-enforced import restriction: consumers must share the import-path prefix above that `internal` segment. For example, `example.com/app/foo/internal/cache` can be imported under `example.com/app/foo`, but not by sibling `example.com/app/bar`. Check the actual prefix before moving packages; “same repository” is insufficient.

Capitalization controls exported identifiers at package scope. Moving closely related files between packages can require public APIs and introduce cycles. Avoid exporting implementation purely to satisfy a folder preference. The Go import graph cannot contain cycles; a cosmetic forwarding package does not fix that design problem.

Keep interfaces where consumers need a behavioral contract, unless the library has an established reason to own them. Do not create an interface per concrete type or one file per method. Use composition at a suitable higher boundary; shared packages should not depend on command startup or their consuming service's private implementation.

## Modules are release/dependency units

A module can contain many packages. Add `go.mod` only when independent versioning, distribution, toolchain/dependency control, or another concrete requirement justifies it. Nested modules change what root module patterns include and require their own verification/release handling. Moving a directory changes its package import path even if the module path is unchanged; external consumers may make that a compatibility change.

`go.work` supports coordinated local development of multiple modules; it is optional. It does not replace each module's dependency declarations and versions. The Go reference cautions that committed workspaces may hide the versions real consumers will use; exclusively co-developed monorepos can justify them with explicit policy. Verify independently consumable modules with workspace mode disabled where relevant, using a command-scoped environment rather than changing a user's global Go settings. Avoid leaving local `replace` directives that make published consumers depend on nonexistent paths.

## Location-sensitive behavior

Keep `_test.go` tests with their package or deliberate external test package. Respect `testdata`, relative fixture paths, `//go:embed`, platform filename suffixes, build constraints, cgo inputs, `go:generate` commands and working directories. Moving a file can alter which targets compile or which resources are embedded. Update generator inputs instead of patching generated output alone.

For an actual restructuring, use existing formatting, package listing, build/vet and focused tests appropriate to the changed graph and supported targets. `go test ./...` from one module does not prove every module in a polyglot repository is covered. Do not create extra modules, workspaces or cross-compilation matrices merely to validate documentation or a simple local placement.
