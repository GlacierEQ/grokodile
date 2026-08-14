from __future__ import annotations

import json
import unittest
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


class PublicTruthTests(unittest.TestCase):
    def test_readme_preserves_independence_and_claim_ceiling(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Not affiliated with, endorsed by, or employed by xAI", readme)
        self.assertIn(TOKEN, readme)
        self.assertIn("not current formal-verification proof", readme)
        for forbidden in (
            "Lean 4 formal proofs mathematically guaranteeing",
            "MCP Tool: `verify_truth_gate()`",
            "Synchronized with APEX Highway mesh",
            "preventing memory leaks",
        ):
            self.assertNotIn(forbidden, readme)

    def test_machine_surface_is_exact_and_non_operational(self) -> None:
        capabilities = json.loads((ROOT / "machine/capabilities.json").read_text())
        state = json.loads((ROOT / "machine/excellence-state.json").read_text())
        contract = json.loads((ROOT / "machine/target-contract.json").read_text())
        self.assertEqual(capabilities["capabilities"], EXPECTED_CAPABILITIES)
        self.assertEqual(capabilities["evidence_state"], TOKEN)
        self.assertFalse(capabilities["operational_authority"])
        self.assertEqual(state["principal_state"], "FUNCTIONAL_CANDIDATE")
        self.assertEqual(
            state["evidence_state"], "IMPLEMENTED_CURRENT_HEAD_NATIVE_PROOF_REQUIRED"
        )
        self.assertFalse(contract["current"]["operational_authority"])
        self.assertFalse(contract["current"]["lean_compiler_proof"])

    def test_lean_source_is_not_presented_as_compiled_proof(self) -> None:
        lean = (ROOT / "lean/TruthGate.lean").read_text(encoding="utf-8")
        self.assertIn("theorem truth_gate_soundness", lean)
        self.assertIn("sorry", lean)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "does not currently carry an exact-head Lean compiler receipt", readme
        )


if __name__ == "__main__":
    unittest.main()
