# Safe structural evolution and verification

## Investigate the actual cost

Look for recurring changes spanning unrelated directories, cycles, unstable shared modules, imports bypassing private APIs, hard-to-locate owners, duplicate behavior, and unnecessarily coupled builds. Read the code and consumers behind the symptom. A deep tree or long file alone is not proof of a defect.

For read-only reviews, record evidence and bounded recommendations without modifying application code/configuration. Maintain a requested report incrementally only at an authorized destination. Mark unverified consumers and operational assumptions clearly. Do not invent owners or require a new architectural governance system to conduct an audit.

## Bound the move

Establish the behavior and contracts that must remain stable, the relevant tests/build commands, current working-tree changes, destination collisions and affected consumers. Use a short before/after path or dependency sketch when it helps review. Keep unrelated feature changes and cosmetic reorganizations out of the move.

Search both symbol imports and path-based consumers. Depending on the change, include:

- Public exports, dynamic imports/requires, file globs, reflection, plugin registration, route discovery and framework special files.
- Generator definitions, templates, `part` files, checked-in generated imports and source-map paths.
- Asset/font/localization paths, snapshots/fixtures, Go embeds/build tags, Flutter native references and package-qualified resources.
- Migration discovery paths and applied migration identities; relocating files must not make old migrations run as new ones.
- Container build contexts/copy rules, deployment entrypoints, CI working directories/path filters, code-owner rules, package publication allowlists and ignored outputs.
- Configuration discovery/inheritance and relative paths resolved from a config file, module URL or process working directory.

Avoid blind global string replacements: the same path text can be a URL, fixture, generated identifier or unrelated app reference. Check case-sensitive targets even on Windows/macOS. Case-only renames may need a checked temporary name on a case-insensitive filesystem. Do not overwrite an existing destination or user changes.

## Preserve the public surface

A package/file import path may be an API for other repositories, generated clients, configuration loaders or consumers not visible in the local tree. Absence of local imports is not proof that a published entrypoint is unused.

Update internal callers together. When a supported public path must change, consider a narrow compatible forwarding export, re-export or migration appropriate to the ecosystem. Check that a shim does not introduce cycles, side effects, duplicate instances, or server/client contamination. Keep compatibility only where there is an actual contract to preserve; do not add wrappers to every move.

Preserve runtime initialization and resource/state lifetimes. A refactor that creates a second client singleton, relocates a provider, changes config loading order, or shifts a routing boundary changes behavior. Do not call it a pure file move. For risky changes, define a reversible sequence and compatibility window rather than doing a repository-wide rewrite.

## Place supporting files with their owner

Follow existing runner conventions for colocated or centralized tests and fixture roots. Keep feature-specific test helpers local and share only suitable stable test infrastructure. Avoid tests coupled to private organization rather than observable contracts.

Keep generation inputs, generator versions/commands, and generated outputs distinguishable. Some generated source is intentionally committed; build products and local caches usually are not. Inspect policy instead of adding blanket ignore rules. Protect secrets, signing keys and real credentials; sanitized environment examples should communicate configuration without secret values.

Put migration files, API schemas, deployment configuration and infrastructure with their operational owner. Do not duplicate them across applications just to make each directory look self-contained. Preserve required root configuration and tool discovery locations.

## Enforce only useful boundaries

Reuse native visibility and installed checks: Go `internal`, explicit JS package entrypoints, Dart implementation-import rules, and relevant existing lint/build constraints. ESLint `no-restricted-imports` covers static imports, not every dynamic load; TS aliases/references are not a security boundary. Nx JS import rules and its broader graph/conformance capabilities have different scope and licensing requirements. Verify available versions/features before recommending them.

When changing a boundary rule, check a representative forbidden edge and a legitimate edge so it detects the intended violation without blocking valid work. This is a focused rule check, not a requirement to build a custom analyzer or evaluation harness. CODEOWNERS coordinates review; it is not authorization or import enforcement.

## Verify what moved

Choose existing checks based on the affected contracts: import/type analysis, relevant package tests, route/build verification, generator checks, consumed package contents or a deployment-artifact smoke check. Verify packaged/deployed resolution when the move changes that boundary. A development server or textual search alone cannot establish those properties.

Review the final diff and status for accidental deletions, stale references, empty abstractions, new cycles, leaked artifacts and unrelated modifications. Keep moves and content changes reviewable; Git can detect renames from content similarity without a special history-preserving rewrite. Report actual commands/outcomes and any untested consumers/platforms. Do not add broad fixtures, repeated full builds or benchmark campaigns when normal focused verification is sufficient.
