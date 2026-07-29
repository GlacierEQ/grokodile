"""Test suite for Grokodile Modules (truth_gate, session_hygiene, tool_allowlist, handoff_pack)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from truth_gate import check
from session_hygiene import SessionState, compact_session
from tool_allowlist import ToolGate
from handoff_pack import HandoffPackage

class TestGrokodileTruthGate(unittest.TestCase):
    def test_truth_gate_valid_text(self):
        res = check("Portfolio motion for SpaceX-class thermal problems")
        self.assertTrue(res.ok)
        self.assertEqual(len(res.hits), 0)

    def test_truth_gate_forbidden_claim(self):
        res = check("I worked at SpaceX as principal GNC")
        self.assertFalse(res.ok)
        self.assertTrue("I worked at SpaceX" in res.hits[0])

class TestGrokodileSessionHygiene(unittest.TestCase):
    def test_session_compaction(self):
        state = SessionState(session_id="test-session-01", tokens_used=100000, token_limit=128000)
        self.assertTrue(state.requires_compaction)
        res = compact_session(state)
        self.assertTrue(res["compacted"])
        self.assertEqual(res["status"], "COMPACTION_SUCCESS")

class TestGrokodileToolAllowlist(unittest.TestCase):
    def test_tool_gate_authorization(self):
        gate = ToolGate()
        self.assertTrue(gate.is_allowed("view_file"))
        self.assertFalse(gate.is_allowed("unauthorized_cmd"))
        res = gate.authorize("run_command", {})
        self.assertTrue(res["authorized"])

class TestGrokodileHandoffPack(unittest.TestCase):
    def test_handoff_package_compile(self):
        pkg = HandoffPackage(task_name="Grokodile Polish Pass", modified_files=["src/truth_gate.py"])
        compiled = pkg.compile()
        self.assertEqual(compiled["task_name"], "Grokodile Polish Pass")
        self.assertEqual(compiled["handoff_status"], "READY_FOR_IC_HANDOFF")

if __name__ == "__main__":
    unittest.main()
