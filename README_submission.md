# Lab 17 — Submission Notes

Final practice run: **11/11 PASS**, hit rate 1.00, avg latency 827.6 ms, avg token reduction 20.6% (`reports/benchmark.json`).

## A. Reflection

**1. Most important layer in this test set.** Long-term. It carries E02, E03, E08 and E09 (20 auto points, more than any layer) plus the `Python` half of E07. It owns the hardest behaviours: scoped recency (E08) and isolation (E09), where a wrong `user_id` is a data-leak bug, not just a miss.

**2. Zep Context Block vs Redis + Qdrant.** Zep gave managed user/thread graphs, cross-session relevance and temporal/scoped facts with little plumbing: E08 returned the newer BLUEBIRD-42 constraint without conflict-resolution code, and isolation followed from `user_id` scoping. Costs: managed-service dependence, an opaque ranker, ~1.4 s latency vs ~0 ms locally. Redis + Qdrant give explicit control of storage, indexing and ranking plus portability, but I would build extraction, recency/validity and per-user namespacing myself — where isolation bugs appear.

**3. Guardrail against memory poisoning.** Gate durable writes behind consent (`data/consent.json`, `require_memory_consent`) and minimise PII at ingestion. Keep user memory and the shared semantic graph separate so one user's text cannot become domain policy — verified: personal markers never appeared in shared-graph results. Retain provenance (source, timestamp, validity per `MEMORY_SCHEMA.md`) so facts are superseded, not silently rewritten, and never let a heartbeat grant itself new permissions (`AGENTS.md`).

## B. Benchmark analysis

1. **Lowest hit rate:** none — all five layers tie at 100% (short_term 2/2, long_term 4/4, episodic 2/2, semantic 2/2, mixed 1/1). No layer underperformed.
2. **Most tokens retrieved:** E08, long_term, 721 tokens (then E02 715, E03 714) — Context Blocks are richer than graph-search snippets.
3. **E07 (mixed)** combines long-term personal memory (`Python`) with shared semantic knowledge (`Idempotency-Key`). ContextBudgetManager must preserve both: long-term was trimmed 720→324 tokens, yet `Python` survived because trimming keeps the head.
4. **Token reduction:** 20.6% with memory vs 81.8% without — but no-memory scores only 2/11 (18.2%). It looks efficient because it retrieves almost nothing, so reduction is meaningful only alongside hit rate.

## C. Notes

**E08:** BLUEBIRD-42 → TypeScript/NestJS coexists with ORCHID-27 → Python; the update is project-scoped, not a global overwrite.

**E10:** `REVIEW-DEADLINE-1600` / Friday / 16:00 survived 8 compactions as a durable note after the raw turn was evicted.
