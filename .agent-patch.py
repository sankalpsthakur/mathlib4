from pathlib import Path

source_path = Path("Mathlib/Tactic/Lift.lean")
source = source_path.read_text()

old_type = """  let (p, coe, inst) ← Lift.getInst (← inferType e) (← Term.elabType t)
"""
new_type = """  let newType ← Term.elabType t
  let (p, coe, inst) ← Lift.getInst (← inferType e) newType
"""
if source.count(old_type) != 1:
    raise SystemExit(f"expected one Lift.getInst call, found {source.count(old_type)}")
source = source.replace(old_type, new_type, 1)

old_syntax = """  let prfEx ← instantiateMVars prfEx
  let prfSyn ← prfEx.toSyntax
"""
new_syntax = """  let prfEx ← instantiateMVars prfEx
  let prfSyn : Term := ⟨← prfEx.toSyntax⟩
  let prfSyn ← `(term| (show ∃ _ : $t, _ from $prfSyn))
"""
if source.count(old_syntax) != 1:
    raise SystemExit(f"expected one proof-to-syntax conversion, found {source.count(old_syntax)}")
source_path.write_text(source.replace(old_syntax, new_syntax, 1))

test_path = Path("MathlibTest/Tactic/Lift.lean")
test = test_path.read_text()
regression = """

-- Regression test for https://github.com/leanprover-community/mathlib4/issues/15865.
abbrev MyNat := ℕ

namespace MyNat

theorem isTrue (_ : MyNat) : True := trivial

end MyNat

example (n : ℤ) (hn : n ≥ 0) : True := by
  lift n to MyNat using hn
  exact n.isTrue
"""
if "issues/15865" in test:
    raise SystemExit("lift abbreviation regression already present")
test_path.write_text(test.rstrip() + regression + "\n")
