# Ownership, placement, and extraction

## Decide from responsibility

Find the existing implementation and callers, not just a familiar folder name. Describe the unit in domain terms: “invoice calculation,” “HTTP transport,” or “order-list selection,” rather than “helper.” Identify who changes it, which runtime executes it, and what it owns. A name such as `services` can mean different things across frameworks.

| Choice | Evidence that justifies it |
| --- | --- |
| Keep in the same file | One coherent concept, local use, and easier reasoning together |
| Extract beside the caller | A distinct responsibility, independent tests, or repeated local use |
| Add a feature subdirectory | A meaningful group of related files whose ownership becomes clearer |
| Use an application-level shared module | Several features need the same stable behavior within this application |
| Create a package | An intentional consumption/API boundary, real consumers or distribution/build benefit, and a maintainable contract |
| Create a deployable service | Operational, security, scaling, or ownership requirements justify independent execution and its distributed-system costs |

Do not escalate through this table mechanically. A single-file change may be the complete solution.

Feature-first organization improves locality for changes spanning UI, state, validation, and integration. Layer-first organization can be clear in a small service or a cohesive technical subsystem. A hybrid can keep feature behavior together while sharing genuinely common infrastructure. Preserve a suitable existing choice; address observed change friction rather than naming differences.

## Interpret common directory names locally

The following are responsibility cues, not folders to create. Unless genuinely shared, keep these responsibilities within their feature/module owner.

| Names | Appropriate responsibility and boundary |
| --- | --- |
| `features`, `modules` | A cohesive capability and its deliberate public surface; not arbitrary wrappers around every file |
| `components`, `widgets`, `ui` | Presentation units owned by a screen/feature; promote stable, broadly applicable primitives to shared UI |
| `hooks`, `context`, `providers`, `state`, `store` | State/behavior ownership and injection boundaries; match the actual lifetime, not a desire to make everything global |
| `handlers`, `controllers`, `routes`, `middleware` | Transport entrypoints, routing and cross-cutting request behavior; business policy should remain understandable and reusable where needed |
| `services`, `actions` | A named workflow, application capability, or framework-specific action; distinguish orchestration from low-level I/O |
| `repositories`, `clients`, `adapters`, `integrations` | Respectively domain data access, remote protocol access, boundary translation, or an external-system integration; avoid pass-through stacks without a purpose |
| `models`, `types`, `schemas`, `validators` | Owned domain representations, compile-time contracts, runtime/wire schemas, and validation; avoid a global file mixing unrelated domains |
| `utils`, `helpers`, `lib` | Small, well-named capabilities with explicit scope; not an unrestricted home for business logic or mutable process state |
| `config`, `constants` | Typed/validated configuration or stable values owned by their consumers; keep secrets and environment-specific runtime data out of distributable shared code |
| `workers`, `jobs`, `events` | Execution entrypoints, job workflows, or event contracts/handlers; separate deployment ownership from shared processing logic when required |
| `assets`, `styles`, localization resources | Feature/app-owned presentation inputs subject to asset discovery and bundling rules |
| `tests`, fixtures, mocks | Verification for the owning behavior, following existing runner/discovery conventions |
| `scripts`, tooling, infrastructure | An identified development/deployment capability with a clear working directory and affected applications |
| `apps`, `packages` | Deployable applications versus consumable units where this convention fits; neither name makes a directory a package |
| `internal`, `cmd` | Go-specific import visibility and command conventions; do not transplant their meaning into other languages |

## Split and share deliberately

Look for independent reasons to change, unrelated dependency clusters, confusing resource lifetimes, and an extractable cohesive API. A long generated file or a readable business workflow can stay intact. Tiny files that must always be understood together may be better combined. File size is a symptom to investigate, not a threshold to enforce.

Similar syntax does not prove shared semantics. Two discount calculations owned by different products may need independent rules; one date parser with identical contracts and multiple callers may be a sensible shared capability. Consider whether sharing introduces more flags, dependencies, or coordinated releases than it removes duplication. Limited intentional duplication can cost less than a misleading common abstraction.

For a dependency cycle, identify why the concepts depend on each other. Move ownership, compose collaborators at a higher boundary, merge inseparable units, or extract a genuinely stable contract. Moving imports through a `common` package or an index file does not resolve a logical cycle. Avoid interfaces added solely to disguise it.

Make names explain purpose, follow language idioms, and preserve consistent existing naming. Add brief ownership/API documentation only where the boundary would otherwise be ambiguous. Review shared directories for unrelated dependencies and accidental consumers before broadening their public surface.
