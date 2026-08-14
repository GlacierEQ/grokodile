from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from handoff_pack import HandoffPackage
from session_hygiene import SessionState, compact_session
from tool_allowlist import ToolGate
from truth_gate import EVIDENCE_STATE, check


class TestGrokodileTruthGate(unittest.TestCase):
    def test_truth_gate_valid_text(self) -> None:
        result = check("Portfolio motion for SpaceX-class thermal problems")
        self.assertTrue(result.ok)
        self.assertEqual(result.hits, ())
        self.assertEqual(result.evidence_state, EVIDENCE_STATE)
        self.assertFalse(result.semantic_fact_check)
        self.assertFalse(result.operational_authority)
        self.assertEqual(len(result.fingerprint), 64)

    def test_truth_gate_forbidden_claim(self) -> None:
        result = check("I worked at SpaceX as principal GNC")
        self.assertFalse(result.ok)
        self.assertIn("I worked at SpaceX", result.hits[0])

    def test_truth_gate_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            check(None)  # type: ignore[arg-type]


class TestGrokodileSessionHygiene(unittest.TestCase):
    def test_session_compaction_is_deterministic_local_math(self) -> None:
        state = SessionState(
            session_id="test-session-01",
            tokens_used=100000,
            token_limit=128000,
        )
        self.assertTrue(state.requires_compaction)
        result = compact_session(state, compaction_id="TEST_COMPACTION")
        self.assertTrue(result["compacted"])
        self.assertEqual(result["status"], "LOCAL_COMPACTION_APPLIED")
        self.assertEqual(result["remaining_tokens"], 35000)
        self.assertEqual(state.externalized_memories, ["TEST_COMPACTION"])
        self.assertFalse(result["external_memory_written"])
        self.assertFalse(result["operational_authority"])

    def test_invalid_session_budget_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            SessionState(session_id="bad", tokens_used=-1)
        with self.assertRaises(ValueError):
            SessionState(session_id="bad", token_limit=0)


class TestGrokodileToolAllowlist(unittest.TestCase):
    def test_tool_gate_authorization_is_classification_only(self) -> None:
        gate = ToolGate()
        allowed = gate.authorize("run_command", {})
        denied = gate.authorize("unauthorized_cmd", {})
        self.assertTrue(allowed["authorized"])
        self.assertFalse(allowed["executes_tool"])
        self.assertFalse(allowed["operational_authority"])
        self.assertFalse(denied["authorized"])
        self.assertEqual(denied["reason"], "TOOL_NOT_ALLOWLISTED")

    def test_bad_params_fail_closed(self) -> None:
        with self.assertRaises(TypeError):
            ToolGate().authorize("view_file", [])  # type: ignore[arg-type]


class TestGrokodileHandoffPack(unittest.TestCase):
    def test_handoff_package_marks_caller_assertions(self) -> None:
        incomplete = HandoffPackage(
            task_name="Grokodile local proof",
            modified_files=["src/truth_gate.py"],
        ).compile()
        self.assertEqual(incomplete["handoff_status"], "EVIDENCE_INCOMPLETE")
        self.assertEqual(incomplete["verification_source"], "CALLER_SUPPLIED")

        claimed_ready = HandoffPackage(
            task_name="Grokodile local proof",
            modified_files=["src/truth_gate.py"],
            tests_passed=True,
            sha256_verified=True,
        ).compile()
        self.assertEqual(claimed_ready["handoff_status"], "CALLER_ASSERTS_READY")
        self.assertFalse(claimed_ready["operational_authority"])


if __name__ == "__main__":
    unittest.main()
