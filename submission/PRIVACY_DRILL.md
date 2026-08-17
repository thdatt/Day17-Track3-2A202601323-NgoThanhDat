# Privacy Drill — Right to be Forgotten

Run **after** `reports/benchmark.md`, `reports/benchmark.json`, `reports/golden_benchmark.*`
were saved and committed (11/11 practice, 20/20 golden), and **before** any later scored run.
The lab graph was re-seeded immediately afterwards.

## 1. Delete (`submission/privacy_drill.log`)

```
$ docker compose run --rm app python -m src.forget --user-id minh-lab17

Deleting user-scoped memory for 'minh-lab17'...
Redis keys deleted: 0
Zep user absent: True
Redis user keys remaining: 0
Shared semantic KB remains intact because it stores domain knowledge, not user PII.
```

`Redis keys deleted: 0` is expected: this lab's retrieval path never wrote
`lab17:user:minh-lab17:*` keys (Redis is only exercised by the optional
`src.local_baseline` demo). The verification below still proves the namespace is empty.

## 2. Verify only (`submission/privacy_verify.log`)

```
$ docker compose run --rm app python -m src.forget --user-id minh-lab17 --verify-only

Zep user absent: True
Redis user keys remaining: 0
Shared semantic KB remains intact because it stores domain knowledge, not user PII.
```

Both required lines are present:
- `Zep user absent: True`
- `Redis user keys remaining: 0`

## 3. Functional proof of scope (`submission/privacy_proof.log`)

Deletion was verified behaviourally, not just by a status flag — the deleted user's
memory is genuinely unreachable, while everything out of scope survives.

| Target | Result |
|---|---|
| `minh-lab17` long-term | `ApiError` — user no longer exists |
| `minh-lab17` episodic | `ApiError` — user no longer exists |
| `lan-lab17` long-term (control) | intact: `LOTUS-88`, `Java`, `Spring Boot` still retrieved |
| shared semantic graph (control) | intact: `PAYMENT-RULE-3`, `Idempotency-Key` still retrieved |

No marker of Minh's (`ORCHID-27`, `Python`, `ASYNC-FIX-20`, `BLUEBIRD-42`,
`LAB-REPORT-1600`) is retrievable after deletion.

## Why the shared graph is not deleted

`data/consent.json` gates durable ingestion per user (`memory_opt_in`), and
`src/privacy_guard.py` redacts email/phone before any message is stored. Deletion is
therefore scoped to the **user namespace**: the standalone semantic graph holds domain
knowledge (payment policy, incident playbook) with no user PII, and is shared across
users, so erasing one user must not remove it. This is the practical difference between
*user-scoped* memory and *shared domain* memory in the lab architecture.

## Post-drill state

`python -m src.seed` was re-run after capturing this evidence, restoring both synthetic
users and the semantic graph so the golden set can be re-verified.
