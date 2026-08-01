from pathlib import Path

location_path = Path("Mathlib/Util/AtLocation.lean")
location_text = location_path.read_text()
old = """  | Location.targets hyps target => do
    (← getFVarIds hyps).forM atLocal
    if target then atTarget
"""
new = """  | Location.targets hyps target => do
    for fvarId in ← getFVarIds hyps do
      if (← getGoals).isEmpty then break
      atLocal fvarId
    if target && !(← getGoals).isEmpty then atTarget
"""
if location_text.count(old) != 1:
    raise SystemExit(f"expected one explicit-location loop, found {location_text.count(old)}")
location_path.write_text(location_text.replace(old, new, 1))

test_path = Path("MathlibTest/Tactic/NormNum/Basic.lean")
test_text = test_path.read_text()
regression = """

-- Regression test for https://github.com/leanprover-community/mathlib4/issues/28703.
example (h : 0 = 1) (h2 : 0 = 2) : False := by
  norm_num at h h2
"""
if "issues/28703" in test_text:
    raise SystemExit("regression test already present")
test_path.write_text(test_text.rstrip() + regression + "\n")
