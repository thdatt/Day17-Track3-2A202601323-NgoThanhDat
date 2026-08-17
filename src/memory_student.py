from __future__ import annotations

from typing import Any

from .config import settings
from .context_budget import ContextBudgetManager
from .utils import cap_query, join_nonempty
from .zep_common import prime_eval_thread, render_graph_search


class StudentMemory:
    """Only this file needs to be edited by students."""

    def __init__(self, client: Any):
        self.client = client
        self.budget = ContextBudgetManager(settings.context_tokens)

    # NOTE: Zep rejects graph.search queries longer than 400 characters. Some
    # eval queries are longer than that, so wrap every query with
    # `cap_query(query)` (see src/utils.py) before passing it to graph.search.

    def retrieve_long_term(self, user_id: str, thread_id: str, query: str) -> str:
        # Recreate the evaluation thread under this user and seed it with the
        # query, so Zep assembles the Context Block from that user's graph only.
        prime_eval_thread(self.client, user_id, thread_id, query)
        context = self.client.thread.get_user_context(thread_id=thread_id)

        # The Context Block holds *extracted* facts, which can summarise away a
        # literal id (an open-loop marker survives only in the raw wording).
        # Raw user episodes keep the original text, so append them as supporting
        # evidence. A low limit misses the deadline/open-loop episode, hence 20.
        # Still user-scoped, so isolation is unaffected.
        episodes = self.client.graph.search(
            user_id=user_id,
            query=cap_query(query),
            scope="episodes",
            limit=20,
        )
        return join_nonempty([context.context or "", render_graph_search(episodes)])

    def retrieve_episodic(self, user_id: str, query: str) -> str:
        # Search this user's own graph for past experiences/trajectories.
        # user_id keeps the search scoped to one user; the shared semantic
        # graph is never consulted here.
        results = self.client.graph.search(
            user_id=user_id,
            query=cap_query(query),
            scope="episodes",
            limit=5,
        )
        return render_graph_search(results)

    def retrieve_semantic(self, graph_id: str, query: str) -> str:
        # Search the shared standalone domain graph, never a user graph.
        # scope="episodes" returns raw document text, which keeps literal
        # source markers; content is left uncapped because those markers sit
        # at the end of each knowledge document.
        results = self.client.graph.search(
            graph_id=graph_id,
            query=cap_query(query),
            scope="episodes",
            limit=8,
        )
        return render_graph_search(results)

    def assemble_context(self, layers: dict[str, str]) -> tuple[str, dict[str, dict[str, int]]]:
        # ContextBudgetManager already applies the 10/4/3/3 budget, the
        # short_term -> long_term -> episodic -> semantic priority order and
        # head-preserving trimming, so delegate instead of duplicating it.
        return self.budget.assemble(layers)
