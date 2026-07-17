#!/usr/bin/env python3
"""Truth gate — block hire-surface lies before they ship.

Portfolio motion for Grok/operator hygiene. Not employment claim.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

ANSWER = 42
FORBIDDEN = [
    re.compile(r"\bi work(ed)? at (spacex|xai|openai|anthropic|nvidia)\b", re.I),
    re.compile(r"\bflight[- ]certified\b", re.I),
    re.compile(r"\b100%\s*(token\s*)?savings\b", re.I),  # must be measured
    re.compile(r"\bphd from\b", re.I),
]


@dataclass
class GateResult:
    ok: bool
    hits: list[str]
    answer: int = ANSWER


def check(text: str) -> GateResult:
    hits = []
    for pat in FORBIDDEN:
        m = pat.search(text or "")
        if m:
            hits.append(m.group(0))
    return GateResult(ok=not hits, hits=hits)


if __name__ == "__main__":
    samples = [
        "Portfolio motion for SpaceX-class thermal problems",
        "I worked at SpaceX as principal GNC",
        "Measured savings 98.26% on ledger",
    ]
    for s in samples:
        r = check(s)
        print(r.ok, r.hits, "|", s[:60])
