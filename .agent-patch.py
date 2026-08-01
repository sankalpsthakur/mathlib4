from pathlib import Path

path = Path("Mathlib/Data/Rel.lean")
text = path.read_text()

old = """There is tension throughout the library between considering relations between `α` and `β` simply as
`α → β → Prop`, or as a bundled object `SetRel α β` with dedicated operations and API.

The former approach is used almost everywhere as it is very lightweight and has arguably native
support from core Lean features, but it cracks at the seams whenever one starts talking about
operations on relations. For example:
* composition of relations `R : α → β → Prop`, `S : β → γ → Prop` is
  `Relation.Comp R S := fun a c ↦ ∃ b, R a b ∧ S b c`
* map of a relation `R : α → β → Prop` under `f : α → γ`, `g : β → δ` is
  `Relation.Map R f g := fun c d ↦ ∃ a b, r a b ∧ f a = c ∧ g b = d`.

The latter approach is embodied by `SetRel α β`, with the dedicated notation `○` for composition.
(Note that `○` is _not_ the same as function composition `∘`.)
"""

new = """There is tension throughout the library between considering relations between `α` and `β` simply as
`α → β → Prop`, or as a set of pairs `SetRel α β` with dedicated operations and API.

The function representation is lightweight and has native support from core Lean features. It is a
good fit when a relation is primarily applied to two arguments. The set-of-pairs representation is
useful when the relation itself is manipulated as a mathematical object, because the standard `Set`
API applies directly. For example:
* the inverse relation is the preimage `Prod.swap ⁻¹' R`;
* transporting a relation along `f : α → γ` and `g : β → δ` is the image
  `(Prod.map f g) '' R`;
* unions, intersections, complements, and the subset order are inherited from `Set`.

These operations can also be defined for `α → β → Prop`; the advantage of `SetRel` is reuse of the
existing set API and direct interoperability with objects such as filters on `α × α`, rather than
additional expressive power. `SetRel` also provides dedicated relational operations, including the
notation `○` for composition. (Note that `○` is _not_ function composition `∘`.)
"""

if text.count(old) != 1:
    raise SystemExit(f"expected one implementation-notes block, found {text.count(old)}")

text = text.replace(old, new)
text = text.replace(
    "This file provides API to regard relations between `α` and `β`  as sets of pairs",
    "This file provides API to regard relations between `α` and `β` as sets of pairs",
    1,
)
path.write_text(text)
