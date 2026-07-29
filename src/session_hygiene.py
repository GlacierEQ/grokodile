#!/usr/bin/env python3
"""
Session Hygiene Module (src/session_hygiene.py).
Handles ECHO memory externalization and context compaction before context melt.
"""
from dataclasses import dataclass, field
import time

@dataclass
class SessionState:
    session_id: str
    tokens_used: int = 0
    token_limit: int = 128000
    compaction_threshold: float = 0.75
    externalized_memories: list[str] = field(default_factory=list)

    @property
    def usage_ratio(self) -> float:
        return self.tokens_used / max(self.token_limit, 1)

    @property
    def requires_compaction(self) -> bool:
        return self.usage_ratio >= self.compaction_threshold

def compact_session(state: SessionState) -> dict:
    if state.requires_compaction:
        compacted_tokens = int(state.tokens_used * 0.35)
        saved_tokens = state.tokens_used - compacted_tokens
        state.tokens_used = compacted_tokens
        state.externalized_memories.append(f"ECHO_COMPACTION_{int(time.time())}")
        return {
            "session_id": state.session_id,
            "compacted": True,
            "saved_tokens": saved_tokens,
            "remaining_tokens": state.tokens_used,
            "status": "COMPACTION_SUCCESS"
        }
    return {
        "session_id": state.session_id,
        "compacted": False,
        "saved_tokens": 0,
        "remaining_tokens": state.tokens_used,
        "status": "COMPACTION_NOT_NEEDED"
    }
