"""Case Memory Playground — instructor demo for Lab 17 memory strategies.

Tab 1 "Case Memory Playground": load a REAL case from the public practice
dataset, keep chatting for as many turns as you like, and switch between
Buffer / Summary / Sliding (or compare all three) without changing the
conversation. Then ask about something stated much earlier and watch what each
strategy still remembers.

Tab 2 "Classic Strategy Arena": the original fixed REVIEW-DEADLINE compaction
demo, preserved.

Reads the dataset and reuses `src.short_term.ShortTermMemory` and
`src.llm.generate_reply`. It never touches graded retrieval code, never calls
Zep/Redis/Qdrant, and never injects ground-truth markers into memory or model
context — marker data is used only for on-screen observability checks.

Run:

    docker compose run --rm -p 8501:8501 app \\
      streamlit run src/strategy_arena_ui.py --server.address=0.0.0.0

or locally:  streamlit run src/strategy_arena_ui.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Iterable

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pandas as pd
import streamlit as st

from src.config import settings
from src.demo_short_term import MESSAGES as DEMO_MESSAGES
from src.llm import gemini_available, generate_reply
from src.short_term import ShortTermMemory
from src.utils import GOLDEN_PATH, load_dataset, load_json

# Chat model options. `.env`'s GEMINI_MODEL is offered first, but some older
# ids (e.g. gemini-2.5-flash-lite) now return 404 for new keys, so the UI lets
# the instructor pick a live model without editing any graded file.
_MODEL_SUGGESTIONS = ["gemini-flash-lite-latest", "gemini-3.5-flash-lite", "gemini-flash-latest"]
MODEL_CHOICES = list(dict.fromkeys(
    ([settings.gemini_model] if settings.gemini_model else []) + _MODEL_SUGGESTIONS
))
DEFAULT_MODEL = "gemini-flash-lite-latest"

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

DEADLINE_MARKERS = ("REVIEW-DEADLINE-1600", "Friday", "16:00")
ANCHOR_MARKER = DEADLINE_MARKERS[0]

STRATEGIES = ("buffer", "summary", "sliding")
STRATEGY_LABELS = {"buffer": "BUFFER", "summary": "SUMMARY", "sliding": "SLIDING WINDOW"}
STRATEGY_BLURB = {
    "buffer": "Keeps every turn. Never compacts.",
    "summary": "Compacts old turns into a summary, keeps the last 2.",
    "sliding": "Keeps the last K turns plus summary and durable notes.",
}
CHOICE_TO_STRATEGY = {"Buffer": "buffer", "Summary": "summary", "Sliding": "sliding"}
STRATEGY_CHOICES = ["Buffer", "Summary", "Sliding", "Compare All"]

DEFAULT_K = 6
DEFAULT_PRESSURE = 300

# Educational notice per expected layer — prevents misrepresenting the
# architecture. Only short_term cases are genuinely about these strategies.
LAYER_NOTICE = {
    "short_term": (
        "✅ **This case directly tests Buffer / Summary / Sliding behaviour.** "
        "The official benchmark also evaluates it with local short-term memory."
    ),
    "long_term": (
        "ℹ️ **The official benchmark answers this case with Zep long-term memory "
        "(Context Block), not with these strategies.** Here the playground explores "
        "locally what would happen if the same historical facts had to survive "
        "inside short-term conversation memory alone."
    ),
    "episodic": (
        "ℹ️ **The official result for this case comes from episodic Zep graph search** "
        "over the user's past trajectories. The playground only shows whether the same "
        "experience would survive in short-term conversation memory."
    ),
    "semantic": (
        "ℹ️ **This case is answered officially from the shared semantic knowledge graph**, "
        "which is domain knowledge and not part of any conversation. Short-term strategies "
        "are *not expected* to know it unless that information actually appeared in chat."
    ),
    "mixed": (
        "ℹ️ **The official result combines several durable layers** (long-term + semantic). "
        "The playground covers only the short-term component of that mix."
    ),
}

# Generic demo filler. Deliberately contains no evaluation marker, no
# DURABLE_PATTERNS keyword (todo/deadline/constraint/decision/must/preference…)
# and no 6+ character uppercase token, so it cannot become a durable note or
# fake a ground-truth hit.
FILLER_PAIRS = [
    ("Can you review how we handle logging levels in the service?",
     "Use structured logs with a request id and keep noisy debug output out of production."),
    ("What is a clean way to version an API endpoint?",
     "Prefer a path prefix like /v2 and keep older routes alive during migration."),
    ("The spacing in the settings panel looks cramped.",
     "Increase vertical rhythm and align labels to a single baseline grid."),
    ("How many unit tests are reasonable for a small module?",
     "Cover the branches that encode real rules, not every trivial getter."),
    ("Where should I document the retry helper?",
     "Put a short docstring on the helper and one usage example in the module docs."),
    ("Should we cache the config lookup?",
     "Only if profiling shows it is hot; otherwise keep it simple and readable."),
    ("Any tips for naming boolean flags?",
     "Name them for the positive state so double negatives do not appear in conditionals."),
    ("How do we keep migrations reversible?",
     "Write a down step for every up step and test both in staging."),
    ("Is it worth adding type hints everywhere?",
     "Add them at module boundaries first; internal helpers can follow later."),
    ("What log level fits a retryable network error?",
     "Warn on each attempt and raise the level only when the final one fails."),
]

CSS = """
<style>
.block-container { padding-top: 1.8rem; max-width: 1600px; }
.cmp-sub { font-size: 1.03rem; opacity: .75; margin: -.4rem 0 1rem; }
.cmp-pill {
    display:inline-block; padding:3px 12px; border-radius:999px;
    font-size:.75rem; font-weight:700; letter-spacing:.05em;
    border:1px solid rgba(128,128,128,.35); margin:0 6px 6px 0;
}
.cmp-card {
    border:1px solid rgba(128,128,128,.28); border-radius:14px;
    padding:14px 18px; margin-bottom:12px; background:rgba(127,127,127,.06);
}
.cmp-card h4 { margin:0 0 .4rem; font-size:1.05rem; }
.cmp-kv { font-size:.86rem; line-height:1.65; opacity:.88; }
.cmp-kv b { opacity:1; }
.cmp-verdict {
    border-radius:10px; padding:9px 13px; margin:.35rem 0;
    font-size:.88rem; font-weight:600; border:1px solid rgba(128,128,128,.3);
}
.cmp-ok  { background:rgba(22,163,74,.14); }
.cmp-bad { background:rgba(220,38,38,.14); }
.cmp-note { font-size:.85rem; opacity:.8; line-height:1.55; }
.cmp-flow {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size:.85rem; line-height:1.9; opacity:.85;
}
.cmp-origin { font-size:.72rem; opacity:.55; letter-spacing:.04em; }
</style>
"""


# --------------------------------------------------------------------------
# Memory engine helpers (no Streamlit — callable from a plain REPL)
# --------------------------------------------------------------------------

def _contains(text: str, needle: str) -> bool:
    return needle.casefold() in (text or "").casefold()


def build_memory(
    messages: list[tuple[str, str]],
    strategy: str,
    k: int = DEFAULT_K,
    pressure_tokens: int = DEFAULT_PRESSURE,
) -> ShortTermMemory:
    """Replay a full transcript through one fresh ShortTermMemory."""
    memory = ShortTermMemory(
        strategy=strategy, max_recent_messages=k, pressure_tokens=pressure_tokens
    )
    for role, content in messages:
        memory.add(role, content)
    return memory


def snapshot(memory: ShortTermMemory, strategy: str, anchor: str = "") -> dict[str, Any]:
    """Collect real state from a live memory object."""
    rendered = memory.render()
    retained = [(m.role, m.content) for m in memory.messages]
    durable = list(memory.durable_notes)
    marker_hits = {m: _contains(rendered, m) for m in DEADLINE_MARKERS}
    raw_present = bool(anchor) and any(_contains(c, ANCHOR_MARKER) for _r, c in retained)
    return {
        "strategy": strategy,
        "label": STRATEGY_LABELS[strategy],
        "rendered": rendered,
        "stats": memory.stats(),
        "messages": retained,
        "durable_notes": durable,
        "summary": memory.summary,
        "markers": marker_hits,
        "deadline_retained": all(marker_hits.values()),
        "raw_present": raw_present,
        "in_durable": bool(anchor) and any(_contains(n, ANCHOR_MARKER) for n in durable),
        "in_summary": bool(anchor) and _contains(memory.summary, ANCHOR_MARKER),
        "anchor_evicted": bool(anchor) and not raw_present,
        "has_anchor": bool(anchor),
    }


def find_anchor_message(messages: Iterable[tuple[str, str]]) -> str:
    """Return the original turn carrying the tracked deadline constraint, if any."""
    for _role, content in messages:
        if _contains(content, ANCHOR_MARKER):
            return content
    return ""


def run_strategy_comparison(
    messages: list[tuple[str, str]],
    k: int = DEFAULT_K,
    pressure_tokens: int = DEFAULT_PRESSURE,
) -> dict[str, dict[str, Any]]:
    """Feed identical messages to all three strategies and collect real state."""
    anchor = find_anchor_message(messages)
    return {
        s: snapshot(build_memory(messages, s, k, pressure_tokens), s, anchor)
        for s in STRATEGIES
    }


def explain(result: dict[str, Any]) -> str:
    """Data-driven sentence describing how (or whether) the constraint survived."""
    if not result["has_anchor"]:
        return "This conversation contains no tracked constraint marker."
    if result["strategy"] == "buffer":
        if result["raw_present"]:
            return ("The original turn is still stored as raw history — buffer never "
                    "compacts, so nothing has been evicted yet.")
        return "The constraint is no longer in raw history."
    if result["raw_present"]:
        carriers = []
        if result["in_durable"]:
            carriers.append("durable notes")
        if result["in_summary"]:
            carriers.append("the session summary")
        extra = f" It is also mirrored in {' and '.join(carriers)}." if carriers else ""
        return ("The original turn is still inside the recent window, so it has not been "
                "evicted yet." + extra)
    if result["in_durable"] and result["in_summary"]:
        return ("The original raw turn left the recent window, but the constraint survived "
                "in both durable notes and the session summary.")
    if result["in_durable"]:
        return ("The original raw turn left the recent window, but the constraint was "
                "promoted into durable notes and survived.")
    if result["in_summary"]:
        return ("The original raw turn was compacted away; the constraint survives only "
                "through the session summary.")
    return ("The original raw turn was evicted and no durable note or summary kept the "
            "constraint — it is now unrecoverable from this memory.")


def comparison_frame(results: dict[str, dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame([{
        "Strategy": results[s]["label"],
        "Messages Kept": results[s]["stats"]["messages_kept"],
        "Durable Notes": results[s]["stats"]["durable_notes"],
        "Compactions": results[s]["stats"]["compactions"],
        "Estimated Tokens": results[s]["stats"]["estimated_tokens"],
        "Deadline Retained": "✅ Yes" if results[s]["deadline_retained"] else "❌ No",
    } for s in STRATEGIES])


# --------------------------------------------------------------------------
# Dataset helpers
# --------------------------------------------------------------------------

def golden_available() -> bool:
    return GOLDEN_PATH.exists()


def load_dataset_bundle(name: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return (cases, dataset) for the chosen dataset. Golden is never created."""
    practice = load_dataset()
    if name == "Golden Dataset" and golden_available():
        try:
            golden = load_json(GOLDEN_PATH)
        except Exception:
            return [], practice
        # Golden ships evaluations only; user sessions still come from practice.
        return list(golden.get("evaluations") or []), practice
    return list(practice["evaluations"]), practice


def find_user(dataset: dict[str, Any], user_id: str) -> dict[str, Any] | None:
    return next((u for u in dataset.get("users", []) if u["user_id"] == user_id), None)


def display_name(dataset: dict[str, Any], user_id: str) -> str:
    user = find_user(dataset, user_id)
    return (user or {}).get("first_name") or user_id


def case_label(case: dict[str, Any], dataset: dict[str, Any]) -> str:
    who = display_name(dataset, case.get("user_id", "?"))
    desc = (case.get("description") or "").rstrip(".")
    return f"{case['id']} · {case.get('expected_layer','?')} · {who} · {desc}"


def get_case_seed_messages(
    case: dict[str, Any], dataset: dict[str, Any]
) -> tuple[list[dict[str, str]], str, bool]:
    """Resolve a real starting conversation for a case.

    Returns (messages, provenance_note, reconstructed).

    Rule A: `fixture_messages` on the case (E10).
    Rule B: `thread_id` matches a real seeded session (E01, E04/E05, …).
    Rule C: `eval-*` threads have no original transcript — rebuild "relevant user
            history through stage N" from that user's real sessions, clearly
            labelled as reconstructed. Never fabricated.
    """
    # Rule A
    fixture = case.get("fixture_messages")
    if fixture:
        msgs = [{"role": m["role"], "content": m["content"], "origin": "dataset"}
                for m in fixture]
        return msgs, f"Loaded `fixture_messages` from case **{case['id']}**.", False

    user = find_user(dataset, case.get("user_id", ""))
    sessions = (user or {}).get("sessions", [])

    # Rule B
    session = next((s for s in sessions if s["thread_id"] == case.get("thread_id")), None)
    if session:
        msgs = [{"role": m["role"], "content": m["content"], "origin": "dataset"}
                for m in session["messages"]]
        note = (f"Loaded the real seeded session **{session['thread_id']}** "
                f"(stage {session['stage']}) for this case.")
        return msgs, note, False

    # Rule C
    stage = case.get("after_stage", 1)
    msgs: list[dict[str, str]] = []
    used: list[str] = []
    for s in sorted(sessions, key=lambda x: x["stage"]):
        if s["stage"] > stage:
            continue
        used.append(f"{s['thread_id']} (stage {s['stage']})")
        for m in s["messages"]:
            msgs.append({
                "role": m["role"],
                "content": m["content"],
                "origin": f"dataset · {s['thread_id']}",
            })
    note = (
        f"Case thread `{case.get('thread_id')}` is an evaluation thread with no original "
        f"transcript. Showing **relevant user history through stage {stage}** rebuilt from "
        f"{', '.join(used) or 'no sessions'}. "
        "⚠️ Demo history reconstructed from real dataset sessions; this is not an original "
        "eval thread transcript."
    )
    return msgs, note, True


def marker_report(case: dict[str, Any], rendered: str) -> tuple[list[tuple[str, bool]], list[tuple[str, bool]]]:
    """Substring checks over REAL rendered memory. Observability only."""
    required = [(m, _contains(rendered, m)) for m in (case.get("must_contain_all") or [])]
    forbidden = [(m, not _contains(rendered, m)) for m in (case.get("must_not_contain") or [])]
    return required, forbidden


def as_tuples(convo: list[dict[str, str]]) -> list[tuple[str, str]]:
    return [(m["role"], m["content"]) for m in convo]


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------

DEFAULT_STATE = {
    "dataset_name": "Practice Dataset",
    "strategy_choice": "Sliding",
    "k": DEFAULT_K,
    "pressure": DEFAULT_PRESSURE,
    "gen_answers": False,
}


def apply_pending() -> None:
    """Seed defaults and apply queued control changes BEFORE widgets exist."""
    pending = st.session_state.pop("_pending", None)
    if pending:
        for key, value in pending.items():
            st.session_state[key] = value
    for key, value in DEFAULT_STATE.items():
        st.session_state.setdefault(key, value)


def queue(**changes: Any) -> None:
    st.session_state["_pending"] = changes
    st.rerun()


def load_case_into_state(case: dict[str, Any], dataset: dict[str, Any]) -> None:
    msgs, note, reconstructed = get_case_seed_messages(case, dataset)
    st.session_state["convo"] = list(msgs)
    st.session_state["seed_len"] = len(msgs)
    st.session_state["seed_note"] = note
    st.session_state["seed_reconstructed"] = reconstructed
    st.session_state["active_case"] = case["id"]
    st.session_state.pop("last_grounding", None)
    st.session_state.pop("compare_answers", None)


def add_filler(n: int) -> None:
    convo = st.session_state.setdefault("convo", [])
    start = sum(1 for m in convo if m.get("origin") == "filler") // 2
    for i in range(n // 2):
        u, a = FILLER_PAIRS[(start + i) % len(FILLER_PAIRS)]
        convo.append({"role": "user", "content": u, "origin": "filler"})
        convo.append({"role": "assistant", "content": a, "origin": "filler"})


# --------------------------------------------------------------------------
# Rendering helpers
# --------------------------------------------------------------------------

def yn(flag: bool) -> str:
    return "✅ YES" if flag else "❌ NO"


def strategy_metrics(view: dict[str, Any]) -> None:
    s = view["stats"]
    a, b = st.columns(2)
    a.metric("Messages kept", s["messages_kept"])
    b.metric("Durable notes", s["durable_notes"])
    c, d = st.columns(2)
    c.metric("Compactions", s["compactions"])
    d.metric("Est. tokens", s["estimated_tokens"])


def render_memory_check(case: dict[str, Any], rendered: str) -> None:
    required, forbidden = marker_report(case, rendered)
    if not required and not forbidden:
        st.caption("This case declares no required evidence markers.")
        return
    lines = []
    for marker, present in required:
        lines.append(
            f"<code>{marker}</code> &nbsp; "
            + ("✅ currently in rendered memory" if present
               else "❌ not present in rendered memory")
        )
    for marker, absent in forbidden:
        lines.append(
            f"<code>{marker}</code> &nbsp; (forbidden) "
            + ("✅ absent" if absent else "❌ PRESENT — leakage")
        )
    st.markdown(f'<div class="cmp-kv">{"<br>".join(lines)}</div>', unsafe_allow_html=True)
    st.caption(
        "Substring checks over the real rendered memory. They never modify retrieval "
        "or the model context, and are not the official benchmark verdict."
    )


def chat_model() -> str:
    return st.session_state.get("chat_model") or DEFAULT_MODEL


def answer_for(view: dict[str, Any], question: str, history: list[dict[str, str]],
               generate: bool) -> str:
    """Grounded answer from this strategy's memory only. Never uses markers."""
    if not generate:
        return ""
    if not gemini_available():
        return "_(Gemini key not configured — memory evidence shown instead.)_"
    try:
        return generate_reply(view["rendered"], history, question, model=chat_model())
    except Exception as exc:  # noqa: BLE001
        return f"_(Gemini error: {type(exc).__name__}: {str(exc)[:200]})_"


# --------------------------------------------------------------------------
# Tab 1 — Case Memory Playground
# --------------------------------------------------------------------------

def playground_tab(cases: list[dict[str, Any]], dataset: dict[str, Any],
                   strategy_choice: str, k: int, pressure: int) -> None:
    if not cases:
        st.warning("No cases available in this dataset.")
        return

    labels = [case_label(c, dataset) for c in cases]
    default_idx = next((i for i, c in enumerate(cases) if c["id"] == "E01"), 0)
    with st.sidebar:
        chosen = st.selectbox("Case", labels, index=default_idx, key="case_label")
    case = cases[labels.index(chosen)]

    # Reload the seed only when the case changes — strategy switches must NOT
    # reset the conversation.
    if st.session_state.get("active_case") != case["id"] or "convo" not in st.session_state:
        load_case_into_state(case, dataset)

    convo: list[dict[str, str]] = st.session_state["convo"]

    # ---------------- Case card ----------------
    left, right = st.columns([3, 2], gap="large")
    with left:
        st.markdown(
            f'<div class="cmp-card"><h4>Case {case["id"]}</h4><div class="cmp-kv">'
            f'<b>User:</b> {display_name(dataset, case.get("user_id",""))} '
            f'(<code>{case.get("user_id","")}</code>)<br>'
            f'<b>Layer:</b> {case.get("expected_layer","?")}<br>'
            f'<b>Thread:</b> <code>{case.get("thread_id","-")}</code><br>'
            f'<b>Goal:</b> {case.get("description","-")}<br>'
            f'<b>Original evaluation query:</b> {case.get("query","-")}'
            "</div></div>",
            unsafe_allow_html=True,
        )
    with right:
        req = case.get("must_contain_all") or []
        forb = case.get("must_not_contain") or []
        body = "<b>Required evidence:</b> " + (
            " ".join(f"<code>{m}</code>" for m in req) or "—")
        if forb:
            body += "<br><b>Forbidden evidence:</b> " + " ".join(
                f"<code>{m}</code>" for m in forb)
        st.markdown(f'<div class="cmp-card"><h4>Ground truth (display only)</h4>'
                    f'<div class="cmp-kv">{body}</div></div>', unsafe_allow_html=True)

    st.info(LAYER_NOTICE.get(case.get("expected_layer", ""), ""))
    if st.session_state.get("seed_reconstructed"):
        st.warning(st.session_state.get("seed_note", ""))
    else:
        st.caption(st.session_state.get("seed_note", ""))

    # ---------------- Conversation point ----------------
    total = len(convo)
    if st.session_state.get("_len_seen") != total:
        st.session_state["point"] = total
        st.session_state["_len_seen"] = total
    if total == 0:
        st.warning("This case resolved to an empty conversation.")
        return

    upto = st.slider("Conversation point (messages fed to memory)", 1, max(total, 1),
                     key="point")
    fed = convo[:upto]
    seed_len = st.session_state.get("seed_len", 0)
    st.caption(
        f"Feeding {upto} of {total} messages · seed = first {seed_len} · "
        f"K={k} · pressure={pressure} tokens"
    )

    compare_all = strategy_choice == "Compare All"

    # ---------------- Conversation ----------------
    conv_col, insp_col = st.columns([3, 2], gap="large")

    with conv_col:
        st.subheader("💬 Conversation")
        with st.container(height=420):
            for i, msg in enumerate(convo):
                dim = " (not fed to memory)" if i >= upto else ""
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    origin = msg.get("origin", "")
                    tag = "Demo filler" if origin == "filler" else origin or "chat"
                    st.markdown(
                        f'<span class="cmp-origin">{tag}{dim}</span>',
                        unsafe_allow_html=True,
                    )

    # Build the active memory (single-strategy mode) from the canonical transcript.
    anchor = find_anchor_message(as_tuples(fed))
    if compare_all:
        views = run_strategy_comparison(as_tuples(fed), k, pressure)
        active = views["sliding"]
    else:
        strat = CHOICE_TO_STRATEGY[strategy_choice]
        active = snapshot(build_memory(as_tuples(fed), strat, k, pressure), strat, anchor)
        views = {active["strategy"]: active}

    with insp_col:
        st.subheader("🧠 Memory Inspector")
        st.markdown(
            f'<div class="cmp-kv"><b>Strategy:</b> {active["label"]} &nbsp;·&nbsp; '
            f"<b>K:</b> {k} &nbsp;·&nbsp; <b>Pressure:</b> {pressure} tokens</div>",
            unsafe_allow_html=True,
        )
        strategy_metrics(active)
        with st.expander("View current memory", expanded=False):
            st.code(active["rendered"] or "(empty)", language="text")
        with st.expander("Raw recent messages"):
            if active["messages"]:
                st.dataframe(pd.DataFrame(active["messages"], columns=["role", "content"]),
                             width="stretch", hide_index=True)
            else:
                st.caption("(none retained)")
        with st.expander("Session summary"):
            st.code(active["summary"] or "(no summary yet)", language="text")
        with st.expander("Durable notes"):
            st.code("\n".join(f"- {n}" for n in active["durable_notes"])
                    or "(no durable notes)", language="text")

        st.markdown("#### Memory Check")
        render_memory_check(case, active["rendered"])

    # ---------------- Chat input ----------------
    if prompt := st.chat_input(f"Continue the conversation as {display_name(dataset, case.get('user_id',''))}…"):
        convo.append({"role": "user", "content": prompt, "origin": "chat"})
        # Rebuild memory including the new user turn, then ground the reply on it.
        strat = "sliding" if compare_all else CHOICE_TO_STRATEGY[strategy_choice]
        mem = build_memory(as_tuples(convo), strat, k, pressure)
        grounding = mem.render()
        history = [{"role": m["role"], "content": m["content"]} for m in convo[:-1]]
        if gemini_available():
            try:
                reply = generate_reply(grounding, history, prompt, model=chat_model())
            except Exception as exc:  # noqa: BLE001
                reply = (f"_(Gemini error: {type(exc).__name__}: {str(exc)[:300]} — "
                         "try a different chat model in the sidebar.)_")
        else:
            reply = ("_(GEMINI_API_KEY not configured — no model reply. The memory "
                     "supplied for this turn is shown in the inspector below.)_")
        convo.append({"role": "assistant", "content": reply, "origin": "chat"})
        st.session_state["last_grounding"] = {
            "strategy": STRATEGY_LABELS[strat], "memory": grounding,
            "question": prompt, "answer": reply,
        }
        st.rerun()

    last = st.session_state.get("last_grounding")
    if last:
        st.divider()
        st.subheader("🔗 Grounding for the last turn")
        g1, g2 = st.columns(2, gap="large")
        with g1:
            st.markdown(f"**Memory supplied to model** · {last['strategy']}")
            st.code(last["memory"] or "(empty)", language="text")
        with g2:
            st.markdown("**Assistant answer**")
            st.markdown(last["answer"] or "_(none)_")
            st.caption(f"Question: {last['question']}")

    # ---------------- Compare All ----------------
    if compare_all:
        st.divider()
        st.header("⚖️ Compare All Strategies")
        st.caption("Identical canonical conversation replayed through all three strategies.")
        cols = st.columns(3, gap="medium")
        for col, strategy in zip(cols, STRATEGIES):
            view = views[strategy]
            with col:
                st.markdown(
                    f'<div class="cmp-card"><h4>{view["label"]}</h4>'
                    f'<div class="cmp-kv">{STRATEGY_BLURB[strategy]}</div></div>',
                    unsafe_allow_html=True,
                )
                strategy_metrics(view)
                required, _ = marker_report(case, view["rendered"])
                if required:
                    ok = all(p for _m, p in required)
                    css = "cmp-ok" if ok else "cmp-bad"
                    st.markdown(
                        f'<div class="cmp-verdict {css}">Required evidence retained: '
                        f'{"YES" if ok else "NO"}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        '<div class="cmp-kv">' + "<br>".join(
                            f'{"✅" if p else "❌"} <code>{m}</code>' for m, p in required
                        ) + "</div>", unsafe_allow_html=True)
                with st.expander("View rendered memory"):
                    st.code(view["rendered"] or "(empty)", language="text")

        st.markdown("### 🧪 Compare answers to a question")
        q1, q2 = st.columns([3, 1])
        with q1:
            question = st.text_input(
                "Question", key="compare_q",
                placeholder="What was the project name I mentioned at the beginning?",
            )
        with q2:
            st.write("")
            if st.button("Use original evaluation question", width="stretch"):
                queue(compare_q=case.get("query", ""))
        generate = st.toggle(
            "Generate model answers", key="gen_answers",
            help="OFF compares memory evidence only — no Gemini calls.",
        )
        if st.button("🧪 Compare answers", type="primary"):
            history = [{"role": m["role"], "content": m["content"]} for m in fed]
            st.session_state["compare_answers"] = {
                "question": question,
                "rows": [{
                    "label": views[s]["label"],
                    "memory": views[s]["rendered"],
                    "answer": answer_for(views[s], question, history, generate),
                } for s in STRATEGIES],
            }

        res = st.session_state.get("compare_answers")
        if res:
            st.caption(f"Question: **{res['question'] or '(empty)'}** — same question, "
                       "same conversation, three memories.")
            for row in res["rows"]:
                st.markdown(f"#### {row['label']}")
                c1, c2 = st.columns(2, gap="large")
                with c1:
                    st.markdown("**Memory evidence**")
                    st.code(row["memory"] or "(empty)", language="text")
                with c2:
                    st.markdown("**Answer**")
                    st.markdown(row["answer"] or "_(model answers off)_")

        st.markdown("### Comparison")
        st.dataframe(comparison_frame(views), width="stretch", hide_index=True)
        st.markdown("### Token Footprint")
        tokens = {views[s]["label"]: views[s]["stats"]["estimated_tokens"] for s in STRATEGIES}
        st.bar_chart(pd.DataFrame({"Estimated tokens": tokens}), height=240)
        st.caption("Lower token count is not automatically better; recall quality and "
                   "bounded growth matter too.")


# --------------------------------------------------------------------------
# Tab 2 — Classic Strategy Arena (preserved deadline demo)
# --------------------------------------------------------------------------

def classic_tab(k: int, pressure: int) -> None:
    st.subheader("Classic Strategy Arena — Deadline Compaction Demo")
    st.caption("The original fixed teaching fixture: same conversation, three strategies, "
               "tracking whether an old constraint survives compaction.")
    messages = list(DEMO_MESSAGES)
    results = run_strategy_comparison(messages, k=k, pressure_tokens=pressure)

    cols = st.columns(3, gap="medium")
    for col, strategy in zip(cols, STRATEGIES):
        r = results[strategy]
        with col:
            st.markdown(
                f'<div class="cmp-card"><h4>{r["label"]}</h4>'
                f'<div class="cmp-kv">{STRATEGY_BLURB[strategy]}</div></div>',
                unsafe_allow_html=True,
            )
            strategy_metrics(r)
            css = "cmp-ok" if r["deadline_retained"] else "cmp-bad"
            label = "Deadline retained" if r["deadline_retained"] else "Deadline lost"
            st.markdown(f'<div class="cmp-verdict {css}">'
                        f'{"✅" if r["deadline_retained"] else "❌"} {label}</div>',
                        unsafe_allow_html=True)
            if strategy == "sliding":
                if r["deadline_retained"] and r["anchor_evicted"]:
                    st.success("✅ Durable constraint survived after the original turn "
                               f"left the recent window (K={k}).")
                elif r["deadline_retained"]:
                    st.info(f"Deadline retained, but the original turn is still inside "
                            f"the K={k} window — lower K to force eviction.")
                else:
                    st.error("Deadline lost under the current settings.")
            with st.expander("View Rendered Memory"):
                st.code(r["rendered"] or "(empty)", language="text")

    st.divider()
    st.header("What happened to the original deadline?")
    anchor = find_anchor_message(messages)
    if anchor:
        st.markdown(f"> **{ANCHOR_MARKER}** — {anchor}")
    lc = st.columns(3, gap="medium")
    for col, strategy in zip(lc, STRATEGIES):
        r = results[strategy]
        with col:
            st.markdown(f"**{r['label']}**")
            st.markdown(
                f'<div class="cmp-note">'
                f"Raw constraint still present? {yn(r['raw_present'])}<br>"
                f"Durable note contains it? {yn(r['in_durable'])}<br>"
                f"Session summary contains it? "
                f"{'—' if strategy == 'buffer' else yn(r['in_summary'])}<br>"
                f"Rendered memory can recall it? {yn(r['deadline_retained'])}</div>",
                unsafe_allow_html=True,
            )
            st.caption(explain(r))

    st.divider()
    st.header("Comparison")
    st.dataframe(comparison_frame(results), width="stretch", hide_index=True)

    st.header("Token Footprint")
    tokens = {results[s]["label"]: results[s]["stats"]["estimated_tokens"] for s in STRATEGIES}
    st.bar_chart(pd.DataFrame({"Estimated tokens": tokens}), height=250)
    lo = min(tokens, key=tokens.get)
    hi = max(tokens, key=tokens.get)
    spread = (tokens[hi] - tokens[lo]) / tokens[lo] * 100 if tokens[lo] else 0
    m1, m2, m3 = st.columns(3)
    m1.metric("Lowest footprint", lo, f"{tokens[lo]} tokens")
    m2.metric("Highest footprint", hi, f"{tokens[hi]} tokens")
    m3.metric("Spread", f"{spread:.0f}%")
    st.caption("Lower token count is not automatically better; recall quality and bounded "
               "growth matter too.")

    st.divider()
    st.header("Compaction Behavior")
    buffer_tokens = results["buffer"]["stats"]["estimated_tokens"]
    count_rule, token_rule = len(messages) > k, buffer_tokens > pressure
    if count_rule and not token_rule:
        binding = (f"the **message-count rule** ({len(messages)} turns > K={k}). "
                   "Raising the token threshold will not change these numbers.")
    elif token_rule and not count_rule:
        binding = f"the **token rule** (~{buffer_tokens} tokens > {pressure})."
    elif count_rule and token_rule:
        binding = f"**both rules** ({len(messages)} turns > K={k}, ~{buffer_tokens} tokens > {pressure})."
    else:
        binding = "**neither rule** — the conversation is under both limits."
    st.caption(f"Currently binding: {binding}")

    cc = st.columns([1, 1, 1.1], gap="medium")
    for col, strategy in zip(cc[:2], ("summary", "sliding")):
        r = results[strategy]
        s = r["stats"]
        with col:
            st.markdown(f"**{r['label']}**")
            st.markdown(
                f'<div class="cmp-note">Compactions: <b>{s["compactions"]}</b><br>'
                f'Messages retained: <b>{s["messages_kept"]}</b><br>'
                f'Durable notes: <b>{s["durable_notes"]}</b><br>'
                f'Session summary exists: <b>{"yes" if r["summary"] else "no"}</b></div>',
                unsafe_allow_html=True,
            )
    with cc[2]:
        st.markdown('<div class="cmp-flow">Conversation grows<br>↓<br>Pressure detected<br>↓<br>'
                    "Old turns compacted<br>↓<br>Durable information extracted<br>↓<br>"
                    "Recent context retained</div>", unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="Case Memory Playground", page_icon="🧠", layout="wide")
    apply_pending()
    st.markdown(CSS, unsafe_allow_html=True)

    st.title("🧠 Case Memory Playground")
    st.markdown(
        '<div class="cmp-sub">Load a real dataset case, keep chatting, and switch memory '
        "strategies without changing the conversation.</div>",
        unsafe_allow_html=True,
    )

    # ---------------- Sidebar ----------------
    with st.sidebar:
        st.header("⚙️ Control Panel")

        options = ["Practice Dataset"]
        if golden_available():
            options.append("Golden Dataset")
        dataset_name = st.selectbox("Dataset", options, key="dataset_name")
        if not golden_available():
            st.caption("🔒 Golden dataset has not been released.")

        cases, dataset = load_dataset_bundle(dataset_name)

        st.divider()
        seg = getattr(st, "segmented_control", None)
        if seg is not None:
            strategy_choice = seg("Strategy", STRATEGY_CHOICES, key="strategy_choice")
        else:  # pragma: no cover - older Streamlit
            strategy_choice = st.radio("Strategy", STRATEGY_CHOICES,
                                       horizontal=True, key="strategy_choice")
        if strategy_choice is None:  # segmented_control allows deselection
            strategy_choice = "Sliding"
        st.caption("Switching strategy replays the same conversation — it never resets it.")

        k = st.slider("Recent window K", 2, 10, key="k")
        pressure = st.slider("Pressure tokens", 150, 1200, step=50, key="pressure")
        st.caption("Compaction fires when message count exceeds K **or** estimated tokens "
                   "exceed this threshold — whichever comes first.")

        st.divider()
        st.markdown("**Demo filler turns**")
        f1, f2, f3 = st.columns(3)
        if f1.button("+4", width="stretch"):
            add_filler(4); st.rerun()
        if f2.button("+10", width="stretch"):
            add_filler(10); st.rerun()
        if f3.button("+20", width="stretch"):
            add_filler(20); st.rerun()
        st.caption("Generic filler (logging, API design, spacing, testing, docs). Contains "
                   "no evaluation marker — used to push old facts out of the window.")

        st.divider()
        if st.button("↺ Reset", width="stretch"):
            for key in ("convo", "active_case", "point", "_len_seen", "last_grounding",
                        "compare_answers", "compare_q"):
                st.session_state.pop(key, None)
            queue(**DEFAULT_STATE)

        st.divider()
        st.selectbox("Chat model", MODEL_CHOICES,
                     index=(MODEL_CHOICES.index(DEFAULT_MODEL)
                            if DEFAULT_MODEL in MODEL_CHOICES else 0),
                     key="chat_model")
        st.caption("Gemini: " + ("✅ configured" if gemini_available() else "⚠️ not configured")
                   + " · No Zep / Redis / Qdrant calls.")
        if settings.gemini_model and settings.gemini_model != chat_model():
            st.caption(f"`.env` GEMINI_MODEL is `{settings.gemini_model}`; this session "
                       f"uses `{chat_model()}`.")

    tab1, tab2 = st.tabs(["Case Memory Playground", "Classic Strategy Arena"])
    with tab1:
        playground_tab(cases, dataset, strategy_choice, k, pressure)
    with tab2:
        classic_tab(k, pressure)


if __name__ == "__main__":
    main()
