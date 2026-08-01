from pathlib import Path

attr_path = Path("Mathlib/Tactic/Push/Attr.lean")
attr = attr_path.read_text()
marker = """/--
The `push` attribute is used to tag lemmas that \"push\" a constant into an expression.
"""
pull_attr = """/--
The `pull` attribute tags a lemma for use by the `pull` tactic without also making it a `push`
lemma. The theorem should already be oriented in the direction used by `pull`.

For example, tagging `Function.comp_def` with `@[pull]` lets `pull fun _ ↦ _` eta-expand a
composition without making the reverse rewrite available to `push`.
-/
syntax (name := pullAttr) \"pull\" (ppSpace prio)? : attr

@[inherit_doc pullAttr]
initialize registerBuiltinAttribute {
  name := `pullAttr
  descr := \"one-way attribute for pull\"
  add := fun declName stx _kind => MetaM.run' do
    -- Make sure `mkSimpTheoremFromConst` aux declarations are sufficiently visible, as for `simp`.
    withExporting (isExporting := !isPrivateName declName) do
    let prio ← getAttrParamOptPrio stx[1]
    let some head ← isPullThm declName false |
      throwError \"the theorem is not suitable for `pull`\"
    let #[thm] ← mkSimpTheoremFromConst declName (prio := prio) |
      throwError \"couldn't generate a simp theorem for `pull`\"
    pullExt.add (thm, head)
}

""" + marker
if attr.count(marker) != 1:
    raise SystemExit(f"expected one pull-attribute insertion marker, found {attr.count(marker)}")
attr_path.write_text(attr.replace(marker, pull_attr, 1))

push_path = Path("Mathlib/Tactic/Push.lean")
push = push_path.read_text()
old = """attribute [push ←] Function.id_def
"""
new = old + """attribute [pull] Function.comp_def
"""
if push.count(old) != 1:
    raise SystemExit(f"expected one Function.id_def attribute, found {push.count(old)}")
push_path.write_text(push.replace(old, new, 1))

test_path = Path("MathlibTest/Tactic/Push/Basic.lean")
test = test_path.read_text()
insert_before = """section lambda
"""
regression = """section composition

variable {β γ : Type*} (f : α → β) (g : β → γ)

/-- info: fun x => g (f x) -/
#guard_msgs in
#pull fun _ ↦ _ => g ∘ f

end composition

section lambda
"""
if test.count(insert_before) != 1:
    raise SystemExit(f"expected one composition test insertion marker, found {test.count(insert_before)}")
test_path.write_text(test.replace(insert_before, regression, 1))
