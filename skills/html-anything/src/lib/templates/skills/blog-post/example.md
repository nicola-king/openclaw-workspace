← Filebase blog

Engineering

# Why we rewrote our sync engine in Rust

By Mira Hassan · April 22, 2026 · 8 min read

For two years our Go sync engine was good enough. Then video editors started joining the customer list, and the GC pauses we'd been politely ignoring turned into bug reports we couldn't ignore.

The decision wasn't sudden. We'd been watching the GC pause distribution shift for six months before we admitted what the data was telling us. P50 latency was great. P99 was a horror movie. Customers syncing 30 GB of `.psd` files in active editing sessions were the ones writing in.

Rewriting an entire sync engine sounds like the kind of project a startup is told never to do. We did it anyway. Here's how it went, what surprised us, and the parts I'd do differently.

## The trigger: GC pauses we couldn't fix

Go's garbage collector is brilliant. It is also, fundamentally, a tradeoff. Our hot path allocated short-lived buffer slices on every block diff — and at our scale, on a heavy uploader, the collector ran often enough that the P99 pause crept past 50ms.

We tried the usual fixes: pooling buffers with `sync.Pool`, tuning `GOGC`, reducing allocations in the merge path. They each helped a little. None of them got us under 20ms, and the customers we cared about needed under 5.

> "We can't fix this in Go. We can fix it in something without a GC."

Our staff engineer Sasha said this in a meeting in October. He was right. The question wasn't whether to leave Go. It was what to leave it for, and how much we could keep.

## What we kept; what we threw out

The CLI stayed in Go. The control plane stayed in Go. The bit that does block-level diffing in a hot loop on a customer's laptop — that became Rust. The boundary became a single FFI surface with a small, opinionated protocol.

38ms → 4ms

P99 sync latency

62%

Memory drop

11 weeks

From RFC to ship

The numbers above are real and from production. They are also misleading without context: the Rust port doesn't just remove the GC, it also removes a layer of abstraction we'd been carrying since the Go MVP.

## What I'd do differently

One thing: the FFI boundary. We chose `cgo` for symmetry — Go calling Rust feels right when you already have Go everywhere. But the binding ceremony is brittle, and we ate two production incidents from string lifetime mistakes before we wrote a wrapper layer that handled them once.

If I were starting today, I'd reach for `uniffi` or generate the bindings from a schema. The lessons isn't *don't use cgo*; it's *treat the boundary like an external API the moment you cross language families*.

Filebase is hiring engineers who like writing this kind of post. See open roles →