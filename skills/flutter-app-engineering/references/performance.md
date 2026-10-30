# Rendering, startup, memory, and measured performance

Use for actual startup delays, jank, costly scrolling, CPU or memory pressure. Profile a representative journey/device/build; debug-mode behavior and emulator-only observations do not establish release performance.

## Identify the expensive phase

| Symptom | Useful evidence and proportionate direction |
| --- | --- |
| Slow first useful screen | Startup initialization, storage/session reads, plugin setup, first frame versus first content and dependency waits |
| UI-thread frame misses | Build/layout work, parsing/computation, broad state notifications and synchronous work on the main isolate |
| Raster/GPU pressure | Paint/layers, images, clipping/opacity, shaders/engine/backend and platform views |
| Scroll jank | Lazy item creation, image decoding, intrinsic layout, list extent/identity, nested scrolling and update bursts |
| Memory growth | Retained controllers/subscriptions/contexts/state, decoded images, buffers, caches and native/plugin allocations |

Use DevTools timeline/frame and memory evidence to separate these paths. A rebuild does not imply expensive layout/paint or a network request. Frame budget depends on refresh rate: 60 Hz is roughly 16.7 ms, while higher refresh rates leave less time. Interpret build/raster pipelines correctly instead of treating one generic threshold as every device's budget.

Reduce unnecessary work at its owner: localize changing state, reuse stable subtrees where useful, avoid heavy work in build, and choose lazy list/grid/sliver construction for large sets. Predictable extents can help when valid; a guessed fixed extent that clips translated/scaled content is not a safe optimization.

`const` can reduce unnecessary widget work but does not fix bad data ownership or every rendering bottleneck. RepaintBoundary, clipping, opacity/saveLayer, intrinsic measurement and caching all have tradeoffs. Inspect actual expensive operations before adding boundaries or rewriting render objects.

## Assets, animations and engine differences

Decode/display images near needed resolution with supported cache sizing; distinguish compressed network bytes from decoded memory. Bound image/cache retention and avoid eagerly loading full galleries. Keep useful placeholders and failure behavior without loading full media into memory unnecessarily.

Use existing implicit/explicit animation patterns with owned controllers. Scope listeners/rebuilds and pause/dispose unnecessary ongoing animations. Skeleton shimmer and background tickers can consume resources on low-end devices. Do not add decorative animation to conceal latency or disable all motion when a focused fix suffices.

Impeller availability/defaults and platform rendering paths vary by Flutter version, OS and GPU. Investigate the actual backend/device and current migration/bug guidance before toggling engines or introducing shader workarounds. A change that improves one emulator may regress real supported hardware or platform views.

## Async work and isolates

Network waiting is already asynchronous; moving ordinary requests to another isolate is not a default speedup. Consider isolates for demonstrated CPU-heavy parsing/transformation, accounting for startup, message copying/transfer, plugin limitations and result ownership.

Native `compute` uses an isolate; web compute uses the current event loop. Callback/message/result must be sendable where relevant, and captured closures can retain/copy more state than intended. Prefer a simple sendable boundary and the supported API, not a blanket assumption that all closures are forbidden. A long-lived isolate needs justified reuse, error handling, bounded messages and shutdown.

## Verify the actual claim

Use a bounded comparable profile-mode workflow on representative devices, with relevant cold/warm/cache and network conditions. Verify input responsiveness, scrolling and resource cleanup as well as aggregate timing. Memory snapshots/retaining paths can expose Dart retention while native plugin/GPU memory needs additional platform evidence.

Keep diagnostics private and redact user data. Do not run a benchmark campaign for ordinary UI edits or report smoothness from build success. State the measured change and limits, and preserve accessibility, correctness and battery behavior while optimizing.
