from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = "LOCAL_OPERATOR_HYGIENE_NOT_XAI_GROK_OR_AGENT_RUNTIME_AUTHORITY"
EXPECTED_CAPABILITIES = [
    "deterministic-portfolio-claim-pattern-gating",
    "local-tool-name-allowlist-classification",
    "deterministic-caller-session-budget-compaction",
    "caller-asserted-handoff-envelope-serialization",
    "lean-theorem-source-reference-not-compiled-proof",
]


def test_readme_preserves_independence_and_claim_ceiling() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Not affiliated with, endorsed by, or employed by xAI" in readme
    assert TOKEN in readme
    assert "not current formal-verification proof" in readme
    for forbidden in (
        "Lean 4 formal proofs mathematically guaranteeing",
        "MCP Tool: `verify_truth_gate()`",
        "Synchronized with APEX Highway mesh",
        "preventing memory leaks",
    ):
        assert forbidden not in readme


def test_machine_surface_is_exact_and_non_operational() -> None:
    capabilities = json.loads((ROOT / "machine/capabilities.json").read_text())
    state = json.loads((ROOT / "machine/excellence-state.json").read_text())
    contract = json.loads((ROOT / "machine/target-contract.json").read_text())
    assert capabilities["capabilities"] == EXPECTED_CAPABILITIES
    assert capabilities["evidence_state"] == TOKEN
    assert capabilities["operational_authority"] is False
    assert state["principal_state"] == "FUNCTIONAL_CANDIDATE"
    assert state["evidence_state"] == "IMPLEMENTED_CURRENT_HEAD_NATIVE_PROOF_REQUIRED"
    assert contract["current"]["operational_authority"] is False
    assert contract["current"]["lean_compiler_proof"] is False


def test_lean_source_is_not_presented_as_compiled_proof() -> None:
    lean = (ROOT / "lean/TruthGate.lean").read_text(encoding="utf-8")
    assert "theorem truth_gate_soundness" in lean
    assert "sorry" in lean
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "does not currently carry an exact-head Lean compiler receipt" in readme
