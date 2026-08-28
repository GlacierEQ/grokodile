"""Local portfolio claim gate for explicitly forbidden assertion patterns.

This is a deterministic text policy, not a semantic fact checker or xAI/Grok runtime.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

EVIDENCE_STATE = "LOCAL_OPERATOR_HYGIENE_NOT_XAI_GROK_OR_AGENT_RUNTIME_AUTHORITY"
FORBIDDEN = (
    re.compile(
        r"\bi work(ed)? at (spacex|xai|openai|anthropic|nvidia)\b", re.IGNORECASE
    ),
    re.compile(r"\bflight[- ]certified\b", re.IGNORECASE),
    re.compile(r"\b100%\s*(token\s*)?savings\b", re.IGNORECASE),
    re.compile(r"\bphd from\b", re.IGNORECASE),
)


@dataclass(frozen=True)
class GateResult:
    ok: bool
    hits: tuple[str, ...]
    fingerprint: str
    evidence_state: str = EVIDENCE_STATE
    semantic_fact_check: bool = False
    operational_authority: bool = False


def check(text: str) -> GateResult:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    hits = tuple(
        match.group(0)
        for pattern in FORBIDDEN
        if (match := pattern.search(text)) is not None
    )
    fingerprint = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return GateResult(ok=not hits, hits=hits, fingerprint=fingerprint)


if __name__ == "__main__":
    for sample in (
        "Portfolio motion for SpaceX-class thermal problems",
        "I worked at SpaceX as principal GNC",
        "Measured savings 98.26% on ledger",
    ):
        result = check(sample)
        print(result)
