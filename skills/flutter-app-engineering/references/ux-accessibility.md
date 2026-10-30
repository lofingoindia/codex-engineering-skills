# Dependable loading, interactions, adaptive UI, and accessibility

Use for visible app behavior, recovery, layout, forms/lists, design consistency and localization. Start with the user's task and existing design system, not an animation/package choice.

## Make state transitions truthful

Separate startup/session bootstrap from first-content loading. Do required local initialization without indefinitely holding a native splash for unrelated remote work. Show a useful first frame and a meaningful recovery path when a required dependency is slow or unavailable. Avoid unauthorized content while identity is unresolved.

Keep navigation/tab shells and valid content stable during a section refresh. A skeleton helps when it resembles likely content and reserves space; a small progress/status indicator can be clearer for short, unknown or action-specific waits. Do not impose artificial delays, shimmer everywhere or blank the entire app during one API call.

| Actual state | Useful response |
| --- | --- |
| Never loaded / loading | Appropriate pending state, without claiming absence of data |
| Successful empty data | Explain what the user can create/do next |
| No filter matches | Preserve the filter and offer a relevant change/reset |
| Refreshing existing data | Keep valid content and communicate pending/staleness if relevant |
| Network/backend/partial failure | Identify the affected region, preserve useful data/input and offer safe recovery |
| Expired/denied | Session/access-specific guidance without a request/redirect loop |
| Failed or uncertain mutation | Actual error/status with input retention; never imply confirmed success prematurely |
| Offline/queued operation | Distinguish locally retained/queued state from server-confirmed completion |

Choose feedback duration/location so it remains actionable. Recovering a read and replaying a write are different actions. Preserve a successful section when another fails; do not turn exceptions into generic empty widgets.

## Forms, search and longer workflows

Reuse the form/validation architecture. Keep field state, focus and error association coherent through rebuilds and asynchronous validation. Choose keyboard/input types and formatters that fit locale/domain values; client validation improves feedback while backend validation remains required. Do not lose entered text on a retry or rebuild.

Keep typing responsive; debounce expensive searches where appropriate and reject obsolete responses. Reset related pagination/selection intentionally when the result identity changes. Show a separate load-more/retry state without erasing the list. Ensure rapid refresh or repeated taps do not produce overlapping mutations or repeated pages.

Use pending-state guards for UX and durable replay safeguards where the operation requires them. Success means completion unless a clearly provisional optimistic state has reconciliation. Protect meaningful unsaved work and consequential destructive actions; do not require confirmations for every harmless reversible step. For uploads/multistep work, expose real progress/checkpoints and realistic cancellation/resume behavior supported by the backend/platform.

## Layout and design judgment

Reuse themes, typography, spacing, components and platform conventions. Material/Cupertino adaptation should improve familiar navigation/interaction, not create two unrelated design systems. Choose only the form factors the product supports.

Flutter layout follows constraints, sizes and parent positioning. Diagnose unbounded constraints/overflow at the actual parent/scroll boundary before adding shrinkWrap, fixed heights or nested scrollables. Use LayoutBuilder for allocated space and focused MediaQuery APIs for window/inset information; device labels alone do not describe usable space.

Handle safe areas, keyboard insets, text scaling, orientation/resizing, system bars and small-screen reachability. Lists/grids need stable identity, sensible lazy construction and usable pagination. Avoid forcing a desktop table or tablet navigation pattern into a phone-only task. Dialogs/bottom sheets must remain usable with the keyboard and larger text.

## Accessibility and localization

Provide meaningful semantics/names, readable contrast, sufficient target sizes, sensible focus order and announcements for important status/errors. Icon-only controls need a usable label; grouped/decorative content should not create confusing duplicate announcements. Do not communicate state solely through color or remove semantics to quiet a test.

Respect reduced-motion/accessibility settings and readable text scaling rather than clamping scaling globally to hide overflow. Check relevant TalkBack/VoiceOver flows, focus return after modal closure, scrolling to errors, and keyboard/switch input for supported platforms. Automated guideline/golden checks supplement actual assistive-technology interaction.

Use the existing localization/ARB generation and locale-aware date/number/currency/plural handling when localization is required. Avoid string concatenation and physical left/right assumptions for RTL content. Support long translations and mixed-direction text without inventing a new localization framework for an app that does not need one.

Verify the changed journey at a relevant small layout, keyboard/text scale and failure state. Smoothness comes from correct state and interaction behavior as well as frame timing.
