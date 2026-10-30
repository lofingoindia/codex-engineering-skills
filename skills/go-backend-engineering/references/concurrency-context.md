# Concurrency, contexts, and ownership

Use for goroutine leaks, cancellation, shared state, fan-out, channels/locks or ordering bugs. Establish the business invariant and owner before selecting primitives.

## Separate the failure classes

A data race is an unsynchronized conflicting memory access. A race-free program can still double-process work, violate an invariant, deadlock, starve, lose ordering, or leak resources. Identify the required happens-before relationship and the durable state boundary; passing `-race` does not establish either automatically.

| Requirement | Simple mechanism to consider |
| --- | --- |
| Protect a small shared in-process invariant | A mutex around the complete relevant state transition |
| Transfer work/ownership or coordinate stages | Channels with clear sender/receiver/closure and cancellation lifetimes |
| Independent counters or a proven immutable snapshot | Suitable atomics with documented publication and lifetime |
| Wait for owned tasks | An existing task group or WaitGroup, plus explicit error/cancellation policy |
| Coordinate across processes or survive failure | The actual database/broker/durable protocol; a Go mutex is insufficient |

An RWMutex, sync.Map, atomics or channels are not automatically better than a plain mutex. Several individually atomic fields do not make a multi-field invariant atomic. Avoid holding locks over unrelated slow I/O, define lock ordering, and do not copy mutex/WaitGroup/atomic-bearing values after use. Shared maps, slice backing arrays, pointed-to values and reused buffers can race even when their container was copied.

## Own and bound goroutines

For every new goroutine, identify its owner, error path, stop signal, maximum lifetime, and completion wait. Cancellation followed by immediate return can leave work/resources alive. Track and join owned work where the lifecycle requires it; Go does not kill a goroutine when its parent returns.

Bound active work and queued work independently at the constrained resource. Acquiring capacity inside a newly launched goroutine can still create unlimited waiting goroutines. Buffered channels limit slots, not necessarily retained bytes or blocked producers. Account for all replicas and downstream pool/rate limits. A simple sequential path is often sufficient.

Use a WaitGroup only for lifetime coordination, not error propagation. With Add/Done, add tasks before starting them and before a Wait can observe an empty group; pair completion on every path. Supported `WaitGroup.Go` can simplify task accounting, but does not provide errors/cancellation and its function must not panic. Do not invoke it through another unnecessary `go` statement.

An existing `errgroup` can coordinate sibling failures. Its derived context is canceled when Wait returns even on success; do not use that context for follow-up work after Wait. SetLimit may block submission; nested submission into a full group can deadlock. Cancellation-aware admission and a bounded backlog remain design responsibilities. Do not add a task framework for two straightforward operations.

## Channel and select semantics

Define which sender/coordinator closes a channel after all sends finish. A receiver should not close a channel to tell unknown producers to stop. Sending to a closed channel panics; a nil channel disables a select case; receiving from a closed channel yields the zero value and `ok == false`. Handle closure to avoid a busy loop or false data.

Make blocking sends/receives cancellation-aware where an owner can stop early. `select` does not prioritize cancellation when other cases are ready; a cancellation case alone is not a strict no-further-work guarantee. Tie consequential effects to the actual authorized/durable state transition. Buffering a pipeline merely hides a leak if upstream cannot stop after downstream exits.

Timers and callback stopping have version-specific contracts. Stopping a timer/cancellation callback does not necessarily wait for an already-running callback. Do not copy stale timer-channel drain recipes across toolchains; verify who receives and who stops/resets. Avoid spinning `default` cases and sleeps as synchronization.

## Context is a lifetime signal, not a kill switch

Pass the request/job context explicitly through relevant calls, normally as the first argument; avoid storing request contexts in long-lived structs or using values for general dependencies/optional parameters. Context is safe for concurrent use; values stored in it may still be mutable and unsafe.

Propagate the remaining parent deadline rather than restarting a full budget on each dependency/retry. Call returned cancel functions to release resources when work ends early. Check actual dependency behavior: a Context parameter does not prove it can interrupt blocked I/O or native work. CPU loops and context-unaware operations need their own safe stop points or supported interruption.

Do not “fix” a blocked call by abandoning a goroutine on timeout. Arrange real completion/interruption and ownership. Context cancellation and rollback are distinct from completed remote side effects; a timed-out write may have committed.

`context.WithoutCancel` removes the parent's cancellation/deadline and has a nil Done channel. Use it only for a justified independently bounded lifetime; it neither creates a durable job nor preserves the original timeout. Cleanup that must run after request cancellation may need a separate bounded context, according to the client's contract. Avoid arbitrary background contexts that make ordinary requests immortal.

## Focused verification

Coordinate the affected interleaving explicitly: cancel before admission, stop a receiver while producers are blocked, race two updates to one invariant, fail one sibling, or shut down during work. Assert outcomes and task/resource completion. Use channels/barriers or supported synctest where appropriate; arbitrary sleeps and a single clean race run are weak evidence. Keep test state disposable and scope checks to the changed behavior.
