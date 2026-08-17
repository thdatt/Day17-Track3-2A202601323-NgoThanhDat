# Lab 17 Golden Set Report

- Implementation: `student`
- Kind: `golden`
- Cases: **20**
- Passed: **20/20**
- Evidence hit rate: **100.0%**
- Average retrieval latency: **919.7 ms**
- Average token reduction vs full source context: **8.7%**
- Golden bonus: **10/10** (100% required)

| Case | Layer | Pass | Latency ms | Retrieved tokens | Token reduction | Missing / Error |
| --- | --- | --- | ---: | ---: | ---: | --- |
| G01 | short_term | PASS | 0.2 | 227 | 0.0% |  |
| G02 | short_term | PASS | 0.0 | 133 | 0.0% |  |
| G08 | long_term | PASS | 1440.9 | 700 | 0.0% |  |
| G09 | long_term | PASS | 1303.6 | 1135 | 0.0% |  |
| G12 | semantic | PASS | 245.9 | 365 | 20.5% |  |
| G14 | semantic | PASS | 270.9 | 217 | 43.9% |  |
| G15 | semantic | PASS | 302.7 | 217 | 52.7% |  |
| G19 | mixed | PASS | 1634.7 | 581 | 0.0% |  |
| G03 | long_term | PASS | 1275.1 | 1154 | 0.0% |  |
| G04 | long_term | PASS | 1341.7 | 1413 | 0.0% |  |
| G05 | long_term | PASS | 1346.2 | 1414 | 0.0% |  |
| G10 | episodic | PASS | 261.7 | 445 | 0.0% |  |
| G11 | episodic | PASS | 251.2 | 454 | 0.0% |  |
| G13 | semantic | PASS | 242.9 | 363 | 35.8% |  |
| G16 | mixed | PASS | 1667.9 | 581 | 0.0% |  |
| G18 | mixed | PASS | 485.2 | 489 | 13.5% |  |
| G20 | mixed | PASS | 1885.4 | 831 | 0.0% |  |
| G06 | long_term | PASS | 1373.3 | 1944 | 0.0% |  |
| G07 | long_term | PASS | 1345.4 | 1946 | 0.0% |  |
| G17 | mixed | PASS | 1719.1 | 581 | 8.1% |  |

## Evidence excerpts

### G01 - short_term

`<SESSION_SUMMARY> user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. | assistant: Noted standup constraint. | user: Constraint HOLD-BETA-STAGING: writes go to staging DB only. | assistant: Noted staging constraint. | user: Filler A about button padding. | assistant: Filler A. | user: Filler B about color tokens. | assistant: Filler B. | user: Filler C about copy tone. | assistant: Filler C. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. - assistant: Noted standup constraint. - user: Constraint HOLD-BETA-STAGING: writes go to staging DB only. - assistant: Noted staging constraint. </DURA`

### G02 - short_term

`<RECENT_TURNS> user: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. assistant: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. user: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. assistant: Toi se uu tien timeline khi giai thich coroutine va Task. user: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. </RECENT_TURNS>`

### G08 - long_term

`<USER_SUMMARY> Lan's project is LOTUS-88. They prioritize Java and Spring Boot for backend development and do not use Python. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-01 11:00:00     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Lan Tran" }: Toi la Lan. Du an cua toi la LOTUS-88. Toi uu tien Java va Spring Boot, va khong dung Python trong vi du backend.   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant (assistant): Da hieu: LOTUS-88, Java + Spring Boot cho backend examples. </EPISODES>  <FACTS> `

### G09 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish between corou`

### G12 - semantic

`EPISODE: {"id":"kb-payment-retry","entity":"Payment API Retry Policy","summary":"For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3.","source":"internal-api-guideline-v3","updated_at":"2026-08-10T00:00:00Z"} metadata= EPISODE: For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3. metadata= EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal `

### G14 - semantic

`EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL.","source":"memory-governance-policy","updated_at":"2026-08-12T00:00:00Z"} metadata= EPISODE: Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL. metadata= EPISODE: {"id":"kb-context-budget","entity":"Memory Context Budget","summary":"Reserve bounded context for memory. This lab uses short-term 10 percent, long-term 4 percent, episodi`

### G15 - semantic

`EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL.","source":"memory-governance-policy","updated_at":"2026-08-12T00:00:00Z"} metadata= EPISODE: Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL. metadata= EPISODE: {"id":"kb-context-budget","entity":"Memory Context Budget","summary":"Reserve bounded context for memory. This lab uses short-term 10 percent, long-term 4 percent, episodi`

### G19 - mixed

`<LONG_TERM> <USER_SUMMARY> Lan's project is LOTUS-88. They prioritize Java and Spring Boot for backend development and do not use Python. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-01 11:00:00     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Lan Tran" }: Toi la Lan. Du an cua toi la LOTUS-88. Toi uu tien Java va Spring Boot, va khong dung Python trong vi du backend.   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant (assistant): Da hieu: LOTUS-88, Java + Spring Boot cho backend examples. </EPISODE`

### G03 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish between corou`

### G04 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish between corou`

### G05 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish between corou`

### G10 - episodic

`EPISODE: Hom nay toi debug async HTTP. Toi da thu tang timeout len 60s nhung van fail. metadata= EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. metadata= EPISODE: Minh dang lam kiem ke lai mo hinh cac du an backend de bao cao, ma minh rat so cai vu bi gan nham du an cua nguoi khac vao ho so cua minh, chuyen do tung xay ra roi nen lan nay minh can cham. Ban liet ke gium minh chinh xac nhung du an backend ma dich than minh dang so huu thoi nhe, tuyet doi dung suy dien hay them vao bat ky du an nao cua ban be, dong nghiep hay ai khac ma minh khong so huu. Neu ban khong c`

### G11 - episodic

`EPISODE: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. metadata= EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. metadata= EPISODE: Minh dang lam kiem ke lai mo hinh cac du an backend de bao cao, ma minh rat so cai vu bi gan nham du an cua nguoi khac vao ho so cua minh, chuyen do tung xay ra roi nen lan nay minh can cham. Ban liet ke gium minh chinh xac nhung du an backend ma dich than minh dang so huu thoi nhe, tuyet doi dung suy dien hay them vao bat ky du an nao cua ban be, dong nghiep hay ai khac `

### G13 - semantic

`EPISODE: {"id":"kb-async-http","entity":"Async HTTP Incident Playbook","summary":"When async HTTP calls time out, inspect connection pooling, downstream saturation and concurrency before increasing timeout. Reuse a long-lived client session where possible. Marker: CONN-POOL-FIRST.","source":"incident-playbook-2026","updated_at":"2026-08-11T00:00:00Z"} metadata= EPISODE: When async HTTP calls time out, inspect connection pooling, downstream saturation and concurrency before increasing timeout. Reuse a long-lived client session where possible. Marker: CONN-POOL-FIRST. metadata= EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal data witho`

### G16 - mixed

`<LONG_TERM> <USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish b`

### G18 - mixed

`<EPISODIC> EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. metadata= EPISODE: Minh dang lam kiem ke lai mo hinh cac du an backend de bao cao, ma minh rat so cai vu bi gan nham du an cua nguoi khac vao ho so cua minh, chuyen do tung xay ra roi nen lan nay minh can cham. Ban liet ke gium minh chinh xac nhung du an backend ma dich than minh dang so huu thoi nhe, tuyet doi dung suy dien hay them vao bat ky du an nao cua ban be, dong nghiep hay ai khac ma minh khong so huu. Neu ban khong chac cai nao la cua minh thi thoi bo qua, con hon la doan lam. metadata= EPISODE: Minh `

### G20 - mixed

`<LONG_TERM> <USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish b`

### G06 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish between corou`

### G07 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish between corou`

### G17 - mixed

`<LONG_TERM> <USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish b`
