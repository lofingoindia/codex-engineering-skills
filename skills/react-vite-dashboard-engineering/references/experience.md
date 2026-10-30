# Experience and accessibility

Design around what users need to understand and do at each point in a journey. Reuse the project's spacing, type, color, density, and component vocabulary before adding a new visual system. The [source register](sources.md) distinguishes standards from design-system recommendations.

## Loading with continuity

Keep navigation, page context, and unaffected regions mounted. Place loading/error boundaries around independently useful content; a table refetch should not replace the dashboard shell. Avoid unstable keys or conditional trees that remount forms, reset scroll, or destroy drafts during refresh.

For initial structured content with an unknown value but predictable shape, a restrained skeleton can preserve geometry. For a short action, a button-level pending label or small local indicator is usually clearer. Do not skeletonize already usable controls or introduce artificial waiting to showcase animation. Show fast results immediately; delay a transient indicator only if needed to avoid flicker, without delaying the request or the result. Long waits need honest status and a meaningful retry/cancel path, not an endless decorative shimmer ([Carbon loading](https://www.carbondesignsystem.com/building-blocks/core/patterns/loading)).

Reserve realistic dimensions for tables, charts, images, and navigation. Preserve useful same-context data on background revalidation, with a subtle refreshing/stale indication when it matters. Never label previous-filter results as current results, and never retain previous-account data as a placeholder. Show determinate progress only when it measures real progress; distinguish upload bytes from subsequent server processing.

[Suspense](https://react.dev/reference/react/Suspense) handles supported suspending resources, such as lazy code and supported data integrations; ordinary Effect/event-handler fetching does not activate it. Inspect the project's integration and React version before proposing boundaries. A broad fallback can hide already displayed content. Transitions or deferred rendering may keep suitable content visible; they do not make a fetch cache or establish request ordering. Do not freeze a controlled input inside a transition ([useTransition](https://react.dev/reference/react/useTransition)).

## State and recovery are part of the contract

| Observed state | Appropriate response |
| --- | --- |
| Session or first data load unresolved | Honest pending state; no false empty message or premature permission decision |
| Successfully loaded, no records | Explain the absence; offer a relevant creation action only if permitted |
| No matches for active filters | Keep filters visible and offer reset/change; distinguish from an empty account |
| Forbidden | Explain lack of access safely; do not treat as an empty success or send the user through a login loop |
| Missing/deleted resource | Clear unavailable/not-found state and a useful navigation path |
| Network/server failure with no usable data | Contextual failure, retained inputs, and a bounded retry when safe |
| Refresh failed with usable same-context data | Retain data where safe; show refresh failure/staleness rather than destroying the page |
| Some independent widgets failed | Isolate failures and recovery; preserve successful widgets |
| Save failed or outcome uncertain | Retain draft, distinguish validation/conflict/unknown outcome, reconcile before retrying an irreversible action |

An offline browser signal is a hint, not proof of server reachability. Do not silently queue mutations for later without an actual offline-sync contract. Restore focus and useful feedback after recovery. Avoid duplicate global and local toasts for the same failure.

## Forms and actions

Use semantic forms, persistent labels, clear required/optional instructions, and useful field error text. Preserve entered values on validation or transient failure. Link errors to fields and use an error summary/focus placement when a failed submission needs navigation across several fields. Do not validate aggressively while a user is still entering a valid partial value ([GOV.UK error summary](https://design-system.service.gov.uk/components/error-summary/)).

Keep input state local unless it must survive navigation; dirty forms should not be overwritten by background data refresh. Warn before losing meaningful unsaved work where justified, and clear dirty state only after confirmed save. Reuse the installed router's supported navigation blocking; an unload prompt alone does not cover SPA navigation and may not fire reliably. Never persist sensitive drafts casually in browser storage.

Disable or otherwise guard the specific pending action against duplicate mouse/keyboard submission. Keep unrelated actions available. Announce success after the server confirms it, or explicitly label an optimistic state. A toast is insufficient for critical validation or an action requiring recovery. Confirm consequential destructive actions when their scope or irreversibility warrants it; routine reversible actions often work better with undo. Show exactly which entity, count, or tenant an action affects.

For uploads/multi-step work, distinguish local selection, transfer, server validation/processing, completion, and failure. Validate client-side for early feedback while retaining server enforcement. Preserve meaningful per-file/per-step status; retry only failed work when the contract supports it. Long-running operations need a real status source and safe navigation away, not fabricated percentage progress.

## Tables, charts, and layout

Use information hierarchy and progressive detail to prioritize decisions over decoration. Keep units, time ranges/time zones, precision, and freshness clear. Do not invent data to fill a production empty state. Charts need an understandable summary and accessible values; avoid color-only distinctions or misleading axes. Test tooltips and actions without hover.

For ordinary tabular data, prefer native table semantics with headers, an accessible name/caption, and labeled sort/action controls. A grid is a distinct keyboard widget, not a synonym for a styled table; adding `role=grid` requires focus and directional-navigation behavior ([APG table](https://www.w3.org/WAI/ARIA/apg/patterns/table/), [grid](https://www.w3.org/WAI/ARIA/apg/patterns/grid/)). Define selection scope across pages and filters; stable row IDs preserve selection and input state. Keep server/client filtering and totals truthful.

Adapt navigation and dense content to narrow screens without hiding essential actions. Confine necessary horizontal scrolling to a table region rather than the whole dashboard. Support zoom, text expansion, long labels, and an on-screen keyboard. Theme tokens must keep contrast and focus visible in every supported mode.

## Accessible interaction

Use [WCAG 2.2](https://www.w3.org/TR/WCAG22/) as the project's accessibility baseline/target, not a claim that a component library certifies compliance. Check semantic names/relationships, keyboard access, visible unobscured focus, contrast, reflow, target size, errors, and announced status changes. Honor reduced-motion preferences and avoid announcing every skeleton cell or refresh tick.

Reuse sound accessible primitives. In a modal, move focus inside, contain keyboard navigation, make the background inert, provide an accessible title and safe close behavior, and return focus to the trigger or a logical successor ([APG dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)). Distinguish modal drawers from non-modal panels; do not apply a focus trap to everything. Menus, tabs, and comboboxes have different keyboard expectations. Verify portal layering, scroll behavior, and labels after composition; [Radix](https://www.radix-ui.com/primitives/docs/overview/accessibility) or copied [shadcn/ui](https://ui.shadcn.com/docs) code can be broken by custom wrappers.
