"""Deterministic local session-budget compaction model.

This mutates only the caller-provided SessionState. It does not externalize real
memory, inspect an LLM context, or prevent process memory leaks.
"""

from __future__ import annotations

from dataclasses import dataclass, field

EVIDENCE_STATE = "LOCAL_OPERATOR_HYGIENE_NOT_XAI_GROK_OR_AGENT_RUNTIME_AUTHORITY"


@dataclass
class SessionState:
    session_id: str
    tokens_used: int = 0
    token_limit: int = 128000
    compaction_threshold: float = 0.75
    externalized_memories: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.session_id:
            raise ValueError("session_id is required")
        if isinstance(self.tokens_used, bool) or not isinstance(self.tokens_used, int):
            raise ValueError("tokens_used must be an integer")
        if isinstance(self.token_limit, bool) or not isinstance(self.token_limit, int):
            raise ValueError("token_limit must be an integer")
        if self.tokens_used < 0 or self.token_limit <= 0:
            raise ValueError("token counts must be non-negative and limit positive")
        if not 0.0 < self.compaction_threshold <= 1.0:
            raise ValueError("compaction_threshold must be in (0, 1]")

    @property
    def usage_ratio(self) -> float:
        return self.tokens_used / self.token_limit

    @property
    def requires_compaction(self) -> bool:
        return self.usage_ratio >= self.compaction_threshold


def compact_session(
    state: SessionState, *, compaction_id: str = "LOCAL_COMPACTION"
) -> dict:
    if not isinstance(state, SessionState):
        raise TypeError("state must be SessionState")
    if not compaction_id:
        raise ValueError("compaction_id is required")
    if state.requires_compaction:
        compacted_tokens = int(state.tokens_used * 0.35)
        saved_tokens = state.tokens_used - compacted_tokens
        state.tokens_used = compacted_tokens
        state.externalized_memories.append(compaction_id)
        return {
            "session_id": state.session_id,
            "compacted": True,
            "saved_tokens": saved_tokens,
            "remaining_tokens": state.tokens_used,
            "status": "LOCAL_COMPACTION_APPLIED",
            "evidence_state": EVIDENCE_STATE,
            "external_memory_written": False,
            "operational_authority": False,
        }
    return {
        "session_id": state.session_id,
        "compacted": False,
        "saved_tokens": 0,
        "remaining_tokens": state.tokens_used,
        "status": "LOCAL_COMPACTION_NOT_NEEDED",
        "evidence_state": EVIDENCE_STATE,
        "external_memory_written": False,
        "operational_authority": False,
    }
