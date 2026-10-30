# Runtime, memory, and performance diagnosis

Use for evidenced CPU/latency/resource pressure, leaks, allocations, container behavior or profiling. Runtime implementation details explain symptoms; they are not application correctness guarantees or universal tuning recipes.

## Scheduler and capacity

The runtime schedules goroutines (G) on OS threads (M) using execution resources (P). `GOMAXPROCS` limits simultaneous execution of Go code, not goroutine count, total OS threads, open sockets or dependency concurrency. Network polling, blocking syscalls and cgo have different effects. Preemption is not a guarantee that a goroutine meets a business deadline.

CPU-bound parallelism must fit actual CPU quota/affinity and memory; I/O concurrency must fit downstream/pool capacity and operation lifetimes. More goroutines can add queueing, retained memory and contention. Use the simplest sufficient limit, observing admission/queue behavior as well as throughput.

Current Go can select/update container-aware GOMAXPROCS, but language-version compatibility settings and explicit overrides affect this behavior. Inspect quota versus CPU requests, actual runtime settings and existing automaxprocs-style dependencies before adding another control. Do not set host NumCPU or a fixed worker multiplier blindly. Scheduler internals can evolve across releases.

## Diagnose the right bottleneck

| Evidence | Appropriate next investigation |
| --- | --- |
| CPU saturation | CPU profile: hot business code, serialization, compression, GC, logging or native work |
| High latency with modest CPU | Dependency spans, pool wait, queue depth, lock/block contention or throttling |
| Growing goroutines | Repeated goroutine stacks and owners, blocked sends/receives, unfinished requests and subscriptions |
| Sustained retained heap | In-use heap, cache/buffer/object lifetime, goroutine stack roots and large backing allocations |
| High allocation rate with bounded heap | Allocation profile and GC CPU; not automatically a memory leak |
| RSS/container pressure beyond heap | Runtime memory classes, stacks, fragmentation, native/cgo allocations and non-Go memory |

Capture a representative bounded window and compare equivalent workloads, including error behavior and tail latency. CPU, heap, allocation, goroutine, mutex/block profiles and execution traces answer different questions. Enable expensive sampling only when justified; traces can expose scheduling/I/O/GC interactions that an aggregate CPU profile cannot explain.

Supported Go versions may provide a `goroutineleak` profile for provably unreachable blocked work. It detects a subset, not all goroutine leaks; globally reachable abandoned work can escape it. A healthy profile is not proof that every owner terminates.

## Memory and GC judgment

GC manages reachable heap objects, not business lifetimes, file descriptors, sockets or jobs. Stuck goroutines can retain whole request graphs. Slices/subslices, maps, closures, pooled buffers and context values can keep data alive unexpectedly; shallow copies and resetting length do not necessarily release backing storage.

Use escape analysis/profile evidence to explain allocation costs. Fewer allocations are not always faster: copying, pointer-heavy layouts, contention and cache locality matter. Keep straightforward code until a relevant bottleneck is demonstrated. Do not introduce unsafe code or premature buffer pooling to reduce an allocation counter.

`sync.Pool` is a temporary-object reuse facility whose entries may disappear at any time. It is not a bounded resource pool, durable cache or owner of connections. Reused mutable buffers need exclusive ownership, correct reset/secret handling and protection from retaining huge capacities. Never return a buffer while another goroutine or response still uses it.

GOGC trades collection frequency/CPU against heap growth; GOMEMLIMIT is a soft Go-runtime memory target, not a hard process/container RSS cap. Leave headroom for executable/native/cgo/kernel and other memory. A target below the live working set can cause severe GC pressure rather than fix retention. Do not adjust these or force GC on every request to hide a leak.

## Measurement and diagnostic safety

Use the existing profiler, metrics and telemetry. Keep profiles/traces and pprof endpoints private and protected. A blank import of `net/http/pprof` registers on DefaultServeMux; verify what a public server exposes. Diagnostic labels and captured data can contain secrets or tenant/user details; minimize, protect and expire artifacts.

Benchmark only for an actual performance question, with representative inputs, the right build/toolchain, controlled comparison and allocation/latency metrics as relevant. Prevent dead-code elimination and distinguish setup from measured work; supported `testing.B.Loop` or existing b.N style can help without forcing a benchmark rewrite. Race-instrumented results are not normal throughput evidence. Do not claim a production gain from a synthetic microbenchmark or compiler escape report alone.
