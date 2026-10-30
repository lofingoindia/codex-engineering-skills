# TypeScript, JavaScript, and Node.js boundaries

## Resolve as the actual consumer does

Inspect the executing runtime, compiler/bundler, test runner, package manager and pinned versions. Read the nearest `package.json`, package `type`, entrypoints, `exports`/`imports`, TS configuration inheritance, output paths, and workspace dependency declarations. Source, emitted JS, declarations, and distributable assets can have different locations.

- TypeScript `paths` can describe an alias understood by another tool; it does not rewrite emitted specifiers. A successful type check is not proof of Node or consumer resolution. Avoid using `paths` to impersonate workspace packages and bypass their exports.
- Match module resolution to the consumer. Node ESM rules and bundler resolution are different. Native Node ESM relative imports require explicit file extensions; verify the correct extension for the project's emitted-JS or supported direct-TS execution path. Do not change ESM/CommonJS mode as incidental cleanup.
- Each consuming package should declare what it depends on. Root hoisting, symlinks, a sibling's dependencies, or a development loader can hide missing declarations and output files.
- Define package entrypoints and intended subpaths. Adding restrictive `exports` to a previously open package can break deep-import consumers. Preserve supported entrypoints or provide an explicit migration. Exports improve API discipline; absolute paths can bypass them, so they are not a sandbox.
- Check JS and type entrypoints together. A published declaration must not reference unavailable private aliases, files, or another application's source. Use conditional exports only when real runtime/type targets need them; avoid maintaining dual formats without consumers that require them.

Decide whether a shared package ships source or built artifacts based on its consumers. A source package can suit compatible app bundlers; Node execution, external publishing, or heterogeneous toolchains may need built JS, declarations and copied assets. Verify the consumed package shape rather than assuming every consumer compiles sibling source.

## Keep backend responsibilities legible

Reuse the service's framework and existing modules. Express, Fastify, NestJS and custom servers do not have one prescribed directory tree. A small service can keep cohesive handlers and workflows together without controller/service/repository classes for every operation.

Separate responsibilities when useful:

- Entrypoints assemble dependencies, start the HTTP server or worker, and manage shutdown. Avoid a reusable module starting listeners, reading all environment variables, or connecting to a database merely because it is imported.
- Transport handlers adapt requests and responses; named application workflows coordinate business behavior and transactions where that ownership already exists.
- Infrastructure clients own protocol details and connections; persistence integration belongs with its data/workflow owner. Do not create a repository wrapper that contributes no boundary or behavior.
- Workers can reuse a processing capability while retaining their own startup, concurrency and lifecycle configuration. Code reuse does not imply that HTTP and worker processes must deploy together.

Keep configuration parsing at an appropriate composition boundary. Shared libraries can accept explicit dependencies/configuration instead of importing a consuming app's bootstrap module. Avoid turning dependency injection into a container requirement.

## Type and export ownership

Keep a feature's internal types next to its behavior. Move a type to a shared contract only when its meaning and compatibility belong there. Compile-time types do not validate network input. A database record, public API DTO, and UI model need not share one representation.

Use explicit public exports or useful subpath exports where they clarify the API. Barrel files can conceal cycles, import side effects, or mix server and browser modules. They are optional conveniences, not a requirement for each directory. `import type` can remove a runtime dependency but does not make an otherwise inappropriate architectural coupling desirable.

Project references are an optional compilation boundary, not a workspace replacement. When justified, inspect `composite`, declaration outputs, source inclusion, reference edges and build order. `tsc -b` builds references in dependency order; ordinary `tsc` does not automatically build the graph. Reuse an existing bundler/type-check workflow rather than imposing references on every app.

After a boundary change, verify relevant lint/type checks, actual build outputs, and the execution or package-consumption path. Use the installed package manager's supported inspection/packaging commands when needed; avoid publishing as a validation step.
