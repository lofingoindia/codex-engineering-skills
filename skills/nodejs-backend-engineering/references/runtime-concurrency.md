# Runtime, concurrency, and ownership

Use for scheduling, CPU contention, async failures, cancellation, or runaway work. Inspect the actual Node.js version, code path, traffic shape, and container limits before choosing a mechanism.

## Identify where work executes

JavaScript runs on an event-loop thread within each isolate. V8 and native components can perform additional work on other threads. Network readiness is generally handled through the OS; many filesystem, crypto, compression, and `dns.lookup` operations use libuv's shared worker pool. These paths have different bottlenecks.

| Evidence | Likely investigation and proportionate response |
| --- | --- |
| High event-loop delay with CPU-heavy callbacks | Profile synchronous parsing, validation, serialization, regexes, transformations, or logging; reduce work and bound input first |
| Slow asynchronous filesystem/crypto work with a responsive loop | Check worker-pool contention and competing operations; increasing `UV_THREADPOOL_SIZE` consumes resources and is not a universal throughput fix |
| High request latency with low process CPU | Trace downstream latency, connection acquisition, internal queues, and network limits before adding application replicas |
| Large independent CPU tasks genuinely blocking service | Consider bounded reusable worker threads or a separate job/process boundary; include scheduling, serialization, memory, and failure costs |

Promises, `async`, `await`, and `setTimeout` do not move CPU-heavy JavaScript off the event loop. Wrapping a blocking library in a Promise preserves the blocking behavior. Async I/O often avoids a worker thread per operation; do not add JavaScript workers for ordinary network requests.

Recursive `process.nextTick` or microtask scheduling can starve I/O. Yielding through a supported event-loop mechanism can make bounded chunks cooperative; repeated `await Promise.resolve()` is not a fair I/O yield. Timer ordering is context- and version-sensitive, including ESM versus CommonJS. Do not build correctness on a zero-delay timer racing `setImmediate`.

When workers fit, bound the pool and its waiting queue, handle startup/error/exit, and associate each result with the correct task. Account for cloned/transferred data and transfer ownership. Shared memory requires synchronization. Worker threads are not a malicious-code sandbox; choose process/container isolation for that boundary. Keep total parallelism within actual CPU and memory allocations.

## Make asynchronous work owned

For the changed path, identify the owner and termination condition of each child operation. Every started Promise must be awaited, returned, or deliberately supervised with error handling and a lifetime appropriate to the service. EventEmitter callbacks and timers do not automatically forward failures to a surrounding request handler.

- `Promise.all` is useful for a bounded set of independent operations. A rejection does not cancel siblings. Do not start an unbounded batch with `items.map(async ...)` and then attempt to limit it after creation.
- `Promise.allSettled` exposes individual outcomes; it does not impose capacity or make partial success acceptable. Handle each result according to the business invariant.
- Choose sequential execution when ordering, locks, transactions, or downstream limits require it. Bound concurrency and queued work separately; a concurrency limit with an infinite wait list still permits overload.
- Limit at the scarce resource and account for all replicas. Adding several independent limiters or retries can multiply work instead of protecting the dependency.

Single-threaded JavaScript does not make read-modify-write across `await` atomic. In-process locks do not coordinate replicas or survive crashes. Protect durable invariants using database atomicity, constraints, transactions, or the existing appropriate distributed mechanism.

## Cancellation and deadlines

A deadline bounds how long an owner is willing to wait. Cancellation requests that supported operations stop. Neither rolls back completed side effects.

`Promise.race` alone abandons the wait while the losing operation continues. Prefer the dependency's supported AbortSignal, cancellation, or connection-destruction API. Verify that cancellation covers queued work and body consumption as well as initial connection. Some drivers cannot cancel safely; prevent reuse of an uncertain connection according to driver guidance.

Propagate the parent's remaining budget to child work. Where supported, combine caller cancellation and timeouts without resetting the budget at each retry. Check already-aborted signals before starting, handle abort reasons safely, and remove listeners on normal completion too. Clear owned timers in cleanup; `{ once: true }` alone does not remove a listener if abort never happens.

Cancellation must not acknowledge a durable job or launch untracked compensation. Work that must outlive a request needs an explicit durable owner. Detached Promises and unref'ed timers do not supply one.

## Evidence for a runtime change

Choose a focused reproduction: ensure maximum observed in-flight work stays within the intended bound; reject before acquisition; abort while reading; fail one parallel operation; or terminate a worker. Check settled errors and released resources, not only the returned value. Inspect framework-specific async error propagation. Fake timers cannot establish real I/O scheduling, CPU saturation, or memory behavior.
