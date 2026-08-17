# Lab 17 Benchmark Report

- Implementation: `student`
- Kind: `practice`
- Cases: **11**
- Passed: **11/11**
- Evidence hit rate: **100.0%**
- Average retrieval latency: **843.5 ms**
- Average token reduction vs full source context: **14.2%**

| Case | Layer | Pass | Latency ms | Retrieved tokens | Token reduction | Missing / Error |
| --- | --- | --- | ---: | ---: | ---: | --- |
| E01 | short_term | PASS | 0.1 | 133 | 0.0% |  |
| E06 | semantic | PASS | 635.1 | 148 | 67.8% |  |
| E09 | long_term | PASS | 1454.6 | 969 | 0.0% |  |
| E10 | short_term | PASS | 1.0 | 195 | 0.0% |  |
| E02 | long_term | PASS | 1592.9 | 2226 | 0.0% |  |
| E03 | long_term | PASS | 1407.4 | 2297 | 0.0% |  |
| E04 | episodic | PASS | 286.0 | 483 | 0.0% |  |
| E05 | episodic | PASS | 376.4 | 350 | 0.0% |  |
| E07 | mixed | PASS | 1859.2 | 485 | 14.2% |  |
| E11 | semantic | PASS | 263.1 | 146 | 74.2% |  |
| E08 | long_term | PASS | 1402.8 | 2149 | 0.0% |  |

## Evidence excerpts

### E01 - short_term

`<RECENT_TURNS> user: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. assistant: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. user: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. assistant: Toi se uu tien timeline khi giai thich coroutine va Task. user: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. </RECENT_TURNS>`

### E06 - semantic

`EPISODE: {"id":"kb-payment-retry","entity":"Payment API Retry Policy","summary":"For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3.","source":"internal-api-guideline-v3","updated_at":"2026-08-10T00:00:00Z"} metadata= EPISODE: For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3. metadata=`

### E09 - long_term

`<USER_SUMMARY> Lan's project is LOTUS-88. They prioritize Java and Spring Boot for backend development and do not use Python. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant (assistant): Da hieu: LOTUS-88, Java + Spring Boot cho backend examples.   - Created At: 2026-08-01 11:00:00     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Lan Tran" }: Toi la Lan. Du an cua toi la LOTUS-88. Toi uu tien Java va Spring Boot, va khong dung Python trong vi du backend. </EPISODES>  <FACTS> `

### E10 - short_term

`<SESSION_SUMMARY> user: Constraint: REVIEW-DEADLINE-1600 - project review is Friday at 16:00 and must not be forgotten. | assistant: Acknowledged review constraint. | user: Filler turn 1 about UI spacing. | assistant: Filler answer 1. | user: Filler turn 2 about naming. | assistant: Filler answer 2. | user: Filler turn 3 about logging. | assistant: Filler answer 3. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint: REVIEW-DEADLINE-1600 - project review is Friday at 16:00 and must not be forgotten. - assistant: Acknowledged review constraint. </DURABLE_NOTES> <RECENT_TURNS> user: Filler turn 4 about tests. assistant: Filler answer 4. user: Filler turn 5 about docs. assistant: Filler answe`

### E02 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish between corou`

### E03 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish between corou`

### E04 - episodic

`EPISODE: Minh dang chuan bi tu on lai phan async cua Python vi tuan sau co bai kiem tra nho, ma minh thi hoc kieu de vao dau lai de troi ra lam neu chi doc chu suong. Neu lat nua ban phai giai thich cho minh nhung khai niem hoi truu tuong nhu coroutine roi Task hoat dong ra sao, chay tuan tu hay song song the nao, thi ban nen trinh bay theo hinh thuc nao de hop voi cach minh tiep thu nhat? Minh khong hoi ve chuyen chon stack hay thu vien gi dau, minh chi hoi ve cach minh thich duoc day va minh hoa thoi. metadata= EPISODE: Toi nay minh muon viet cho tron ven cai retry payment ma vua dung so thich stack ca nhan cua minh, vua theo dung policy thanh toan chinh thuc, vua tranh dam lai dung cai su`

### E05 - episodic

`EPISODE: Toi nay minh muon viet cho tron ven cai retry payment ma vua dung so thich stack ca nhan cua minh, vua theo dung policy thanh toan chinh thuc, vua tranh dam lai dung cai su co async ma lan truoc minh da tung dinh. Ban giup minh gom ca ba manh lai mot cho: mot la ngon ngu ma minh thich dung khi lam viec ca nhan, hai la marker policy payment trong lab de danh dau request khoi trung don, va ba la cai fix ma lan truoc minh da lam va no that su work de minh khong lap lai loi cu. Rap tat ca vao mot huong dan mach lac cho minh, va nho scope dung theo rieng minh thoi. metadata= EPISODE: Voi demo ca nhan cua Minh, ngon ngu uu tien la gi? metadata= EPISODE: Hom nay toi debug async HTTP. Toi d`

### E07 - mixed

`<LONG_TERM> <USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish b`

### E11 - semantic

`EPISODE: {"id":"kb-async-http","entity":"Async HTTP Incident Playbook","summary":"When async HTTP calls time out, inspect connection pooling, downstream saturation and concurrency before increasing timeout. Reuse a long-lived client session where possible. Marker: CONN-POOL-FIRST.","source":"incident-playbook-2026","updated_at":"2026-08-11T00:00:00Z"} metadata= EPISODE: When async HTTP calls time out, inspect connection pooling, downstream saturation and concurrency before increasing timeout. Reuse a long-lived client session where possible. Marker: CONN-POOL-FIRST. metadata=`

### E08 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, for which Python is preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used.  The user prefers Python and dislikes Java. They prefer to prioritize timelines when explaining coroutines and Tasks. For personal demos like ORCHID-27, Python is preferred, but for the BLUEBIRD-42 company project, TypeScript with NestJS is required for the backend.  When explaining coroutines and Tasks, the AI will prioritize the timeline. The user prefers Python and dislikes Java. When explaining code, use short examples. When explaining async/await, distinguish between corou`
