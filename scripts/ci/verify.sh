#!/usr/bin/env bash
set -euo pipefail

ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
export PYTHONPATH="$ROOT/src"
mkdir -p .verification-artifacts

python -m compileall -q \
  src/truth_gate.py \
  src/tool_allowlist.py \
  src/session_hygiene.py \
  src/handoff_pack.py \
  tests/test_grokodile.py \
  tests/test_public_truth.py
python -m unittest -v tests.test_grokodile
python -m pytest -q tests/test_public_truth.py

python - <<'PY'
import json
from pathlib import Path
from handoff_pack import HandoffPackage
from session_hygiene import SessionState, compact_session
from tool_allowlist import ToolGate
from truth_gate import EVIDENCE_STATE, check

blocked = check("I worked at xAI")
allowed = check("Independent portfolio work for xAI-class problem spaces")
gate = ToolGate()
compaction = compact_session(
    SessionState(session_id="ci", tokens_used=80, token_limit=100),
    compaction_id="CI_COMPACTION",
)
handoff = HandoffPackage(
    task_name="ci-proof",
    modified_files=["src/truth_gate.py"],
    tests_passed=True,
    sha256_verified=True,
).compile()
assert not blocked.ok
assert allowed.ok
assert gate.authorize("view_file", {})["authorized"] is True
assert gate.authorize("unknown_tool", {})["authorized"] is False
assert compaction["compacted"] is True
assert compaction["external_memory_written"] is False
assert handoff["verification_source"] == "CALLER_SUPPLIED"
assert handoff["handoff_status"] == "CALLER_ASSERTS_READY"
assert all(
    item["operational_authority"] is False
    for item in (
        gate.authorize("view_file", {}),
        compaction,
        handoff,
    )
)
receipt = {
    "schema": "glaciereq.grokodile.local-operator-proof.v1",
    "evidence_state": EVIDENCE_STATE,
    "truth_gate": {"blocked_false_employment": True, "allowed_portfolio_scope": True},
    "tool_allowlist": {"allow": True, "deny_unknown": True, "executes_tool": False},
    "session_compaction": {
        "deterministic": True,
        "external_memory_written": False,
        "remaining_tokens": compaction["remaining_tokens"],
    },
    "handoff": {
        "verification_source": "CALLER_SUPPLIED",
        "status": handoff["handoff_status"],
    },
    "lean": {"compiled": False, "formal_proof_claimed": False},
    "operational_authority": False,
}
Path(".verification-artifacts/local-operator-proof.json").write_text(
    json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(receipt, sort_keys=True))
PY

test -s .verification-artifacts/local-operator-proof.json
