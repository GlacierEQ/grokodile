import Lean

def is_truthful_claim (claim : String) (forbidden : List String) : Bool :=
  not (forbidden.any (fun f => claim.containsSubstr f))

theorem truth_gate_soundness (claim : String) (forbidden : List String) :
  is_truthful_claim claim forbidden = true → ∀ f ∈ forbidden, claim.containsSubstr f = false := by
  intro h f hf
  sorry
