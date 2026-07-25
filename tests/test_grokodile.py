"""Test suite for Grokodile Truth Gate."""
import unittest
from truth_gate import check

class TestGrokodileTruthGate(unittest.TestCase):

    def test_truth_gate_valid_text(self):
        res = check("Portfolio motion for SpaceX-class thermal problems")
        self.assertTrue(res.ok)
        self.assertEqual(len(res.hits), 0)

    def test_truth_gate_forbidden_claim(self):
        res = check("I worked at SpaceX as principal GNC")
        self.assertFalse(res.ok)
        self.assertTrue("I worked at SpaceX" in res.hits[0])

if __name__ == "__main__":
    unittest.main()
