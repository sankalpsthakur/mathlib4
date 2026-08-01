from pathlib import Path

source_path = Path("Mathlib/Tactic/Linter/FlexibleLinter.lean")
source = source_path.read_text()
old = """  | .ident _ _ val _ => {.name val}
"""
new = """  | .ident _ _ val _ =>
    ({.name val} : Std.HashSet Stained).insert (.name val.getRoot)
"""
if source.count(old) != 1:
    raise SystemExit(f"expected one identifier case, found {source.count(old)}")
source_path.write_text(source.replace(old, new, 1))

test_path = Path("MathlibTest/Linter/Flexible/Basic.lean")
test = test_path.read_text()
regressions = r'''

/--
warning: `simp at h` is a flexible tactic modifying `h`.
---
info: `exact h.right`
uses `h`, which was modified
-/
#guard_msgs (substring := true) in
example {x₁ x₂ : Nat} {l₁ l₂ : List Nat} (h : x₁ :: l₁ = x₂ :: l₂) : l₁ = l₂ := by
  simp at h
  exact h.right

/--
warning: `simp at h` is a flexible tactic modifying `h`.
---
info: `have h' := h.right`
uses `h`, which was modified
-/
#guard_msgs (substring := true) in
example {x₁ x₂ : Nat} {l₁ l₂ : List Nat} (h : x₁ :: l₁ = x₂ :: l₂) : l₁ = l₂ := by
  simp at h
  have h' := h.right
  exact h'
'''
if "exact h.right" in test:
    raise SystemExit("dotted-local flexible-linter regression already present")
test_path.write_text(test.rstrip() + regressions + "\n")
