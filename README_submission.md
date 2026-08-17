# Lab 17 — Submission Notes

Practice: **11/11 PASS**, hit rate 1.00, avg latency 692.9 ms, token reduction 19.1% (`reports/benchmark.json`). Golden: **20/20**, `perfect: true` (`reports/golden_benchmark.json`).

## A. Reflection

**1. Most important layer in this test set.** Long-term. It carries E02, E03, E08, E09 (20 points, the most of any layer) plus `Python` for E07. It owns the hardest behaviours: scoped recency (E08) and isolation (E09), where a wrong `user_id` is a data-leak bug, not just a miss.

**2. Zep Context Block vs Redis + Qdrant.** Zep gave managed user/thread graphs, cross-session relevance and temporal/scoped facts with little plumbing: E08 returned the newer BLUEBIRD-42 constraint without conflict-resolution code, and isolation followed from `user_id` scoping. Costs: managed-service dependence, an opaque ranker, ~1.4 s latency, and a Context Block that *summarises away literal ids* — golden G04 needed raw-episode search to recover `LAB-REPORT-1600`. Redis + Qdrant give explicit control of storage, indexing and ranking, but I would build extraction, recency/validity and per-user namespacing myself — where isolation bugs appear.

**3. Guardrail against memory poisoning.** Gate durable writes behind consent (`data/consent.json`) and minimise PII at ingestion. Keep user memory and the shared semantic graph separate so one user's text cannot become domain policy. Retain provenance (source, timestamp, validity per `MEMORY_SCHEMA.md`) so facts are superseded, not silently rewritten, and never let a heartbeat grant itself new permissions (`AGENTS.md`). Measured hygiene risk: eval queries ingested by `prime_eval_thread` accumulate in the user graph and crowd out real episodes — re-seed before a scored run.

## B. Benchmark analysis

1. **Lowest hit rate:** none — all five layers tie at 100% (short_term 2/2, long_term 4/4, episodic 2/2, semantic 2/2, mixed 1/1).
2. **Most tokens retrieved:** E02, long_term, 1153 tokens (E03 1054, E08 991) — long-term returns a Context Block *plus* 20 raw episodes, unlike the compact graph-search layers (~150).
3. **E07 (mixed)** combines long-term personal memory (`Python`) with shared semantic knowledge (`Idempotency-Key`). ContextBudgetManager must preserve both: long-term was trimmed 1129→324 tokens, yet `Python` survived because trimming keeps the head.
4. **Token reduction:** 19.1% with memory vs 81.8% without — but no-memory scores only 2/11 (18.2%). It looks efficient only because it retrieves nothing, so reduction matters only with hit rate.

## C. Notes

**E08:** BLUEBIRD-42 → TypeScript/NestJS coexists with ORCHID-27 → Python; the update is project-scoped, not a global overwrite.

**E10:** `REVIEW-DEADLINE-1600` / Friday / 16:00 survived compaction as a durable note after the raw turn was evicted.
