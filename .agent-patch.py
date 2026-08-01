from pathlib import Path

path = Path("Mathlib/Computability/TuringMachine/PostTuringMachine.lean")
text = path.read_text()

marker = """/-- The state transition function. -/
def step [Inhabited Γ] (M : Λ → Stmt Γ Λ σ) : Cfg Γ Λ σ → Option (Cfg Γ Λ σ)
  | ⟨none, _, _⟩ => none
  | ⟨some l, v, T⟩ => some (stepAux (M l) v T)

"""

addition = marker + """@[simp]
theorem step_none_iff [Inhabited Γ] (M : Λ → Stmt Γ Λ σ) (c : Cfg Γ Λ σ) :
    step M c = none ↔ c.l = none := by
  rcases c with ⟨_ | l, v, T⟩ <;> simp [step]

"""

count = text.count(marker)
if count != 1:
    raise SystemExit(f"expected one TM1.step insertion marker, found {count}")
path.write_text(text.replace(marker, addition, 1))
