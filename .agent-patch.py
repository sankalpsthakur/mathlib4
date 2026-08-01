from pathlib import Path

equiv_path = Path("Mathlib/Topology/Algebra/Module/Equiv.lean")
equiv = equiv_path.read_text()
marker = """@[simp]
theorem neg_apply [ContinuousNeg M] (x : M) :
    neg R x = -x := by simp
"""
addition = marker + """
section NegInstance

variable {R₄ : Type*} [Semiring R₄]
  {N₁ N₂ : Type*} [TopologicalSpace N₁] [AddCommMonoid N₁] [Module R₄ N₁]
  [TopologicalSpace N₂] [AddCommGroup N₂] [Module R₄ N₂] [ContinuousNeg N₂]

/-- Pointwise negation of a continuous linear equivalence. -/
instance : Neg (N₁ ≃L[R₄] N₂) where
  neg e := e.trans (neg R₄)

@[simp]
theorem coe_neg_apply (e : N₁ ≃L[R₄] N₂) (x : N₁) : (-e) x = -e x := rfl

end NegInstance
"""
if equiv.count(marker) != 1:
    raise SystemExit(f"expected one continuous-linear-equivalence negation marker, found {equiv.count(marker)}")
equiv_path.write_text(equiv.replace(marker, addition, 1))

ops_path = Path("Mathlib/Analysis/Calculus/ContDiff/Operations.lean")
ops = ops_path.read_text()
start_marker = """-- TODO: define `Neg` instance on `ContinuousLinearEquiv`,
-- prove it from `ContinuousLinearEquiv.iteratedFDerivWithin_comp_left`
theorem iteratedFDerivWithin_neg_apply"""
end_marker = """
theorem iteratedFDeriv_neg_apply"""
start = ops.find(start_marker)
if start < 0:
    raise SystemExit("could not find iteratedFDerivWithin_neg_apply TODO")
end = ops.find(end_marker, start)
if end < 0:
    raise SystemExit("could not find the next negation theorem")
replacement = """theorem iteratedFDerivWithin_neg_apply {f : E → F} (hu : UniqueDiffOn 𝕜 s) (hx : x ∈ s) :
    iteratedFDerivWithin 𝕜 i (-f) s x = -iteratedFDerivWithin 𝕜 i f s x := by
  simpa [Function.comp_def] using
    (-(ContinuousLinearEquiv.refl 𝕜 F)).iteratedFDerivWithin_comp_left f hu hx i
"""
ops_path.write_text(ops[:start] + replacement + ops[end:])
