# Go verification

Use the project's Go version, module/toolchain settings, existing test layout and supported facilities. Table-driven subtests work well for distinct behavior classes; do not turn them into a generic test framework. Give cases diagnostic names and independent mutable state. Check language-version semantics before adding habitual loop-capture workarounds.

Use public outputs/errors and owned resources. `httptest.ResponseRecorder` can verify handler status, headers, body and relevant application effects; it does not open a socket. Use `httptest.Server` or its TLS facilities for actual local client/transport behavior when required, with the real configured client. Neither proves production load-balancer/TLS deployment behavior. Close bodies, servers, pools and subscriptions.

Exercise context cancellation/deadlines, partial body/stream failures and worker shutdown when those affect the change. Coordinate goroutines with channels/barriers and collect results so assertions finish in the test's lifetime. `FailNow`/`Fatal` must not be used to terminate an unrelated worker goroutine as if it terminated the test. Register cleanup for resources acquired; cancel and await owned workers with a bound rather than leaving them alive between tests. Global goroutine counts can include legitimate framework/runtime work and are not a substitute for ownership evidence.

Use `t.Parallel` only with isolated state/resources. Environment/current-directory changes affect the process; the standard library restricts `t.Setenv` in parallel tests or tests with parallel ancestors. Separate external database/queue namespaces per parallel owner or serialize them. A test named “concurrent” that executes all operations sequentially is insufficient.

Where supported, targeted `go test -race` detects memory races on exercised runtime paths. It does not prove absence of logical check-then-act races, deadlocks, leaked goroutines or incorrect database isolation. Assert the business invariant after controlled competing operations as well. Record whether the race detector actually ran and whether the command was supported; do not claim it from a normal build.

For parsers, protocols and suitable pure logic, native fuzz targets can explore malformed/boundary input and domain properties. Bound fuzz duration/resources, retain failing corpus entries and rerun the specific failure as a regression. A fuzz run that found no crash is not proof of semantic correctness. Keep ordinary seed/regression execution distinct from a new fuzz campaign. For fresh external-integration evidence, account for Go test caching and use an appropriate uncached run when necessary.

`testing/synctest` became generally available in Go 1.25 after an incompatible experimental 1.24 API. Use only the installed toolchain's API when it helps deterministic fake-time/quiescence tests. Its controlled bubble is not a substitute for real network, database or process recovery behavior. Do not import a new clock/scheduler abstraction throughout a service solely for one straightforward test.

Sources: [testing](https://pkg.go.dev/testing), [httptest](https://pkg.go.dev/net/http/httptest), [race detector limits](https://go.dev/doc/articles/race_detector), [fuzzing and regression corpus](https://go.dev/doc/tutorial/fuzz), [current synctest rationale/API transition](https://go.dev/blog/testing-time).
