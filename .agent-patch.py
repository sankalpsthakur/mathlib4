from pathlib import Path

path = Path("Mathlib/RingTheory/Coprime/Lemmas.lean")
text = path.read_text()

marker = """theorem Int.isCoprime_gcdB {x y : ℤ} (h : IsCoprime x y) : IsCoprime (x.gcdB y) x := by
  use y, x.gcdA y
  rwa [add_comm, mul_comm, ← Int.gcd_eq_gcd_ab, Nat.cast_eq_one, ← Int.isCoprime_iff_gcd_eq_one]

"""

addition = marker + """/-- If two integers are coprime and their sum is odd, then their sum and difference are
coprime. Equivalently, the original integers have opposite parity. -/
theorem Int.isCoprime_add_sub {m n : ℤ} (hprime : IsCoprime m n) (hparity : Odd (m + n)) :
    IsCoprime (m + n) (m - n) := by
  rw [← IsCoprime.mul_add_right_right_iff, one_mul, add_add_sub_cancel, ← two_mul]
  apply IsCoprime.mul_right
  · simpa [Int.isCoprime_iff_nat_coprime]
  · simpa using hprime.symm.mul_add_right_left 1

/-- The gcd of the sum and difference of coprime integers of opposite parity is one. -/
theorem Int.gcd_add_sub_eq_one {m n : ℤ} (hprime : IsCoprime m n) (hparity : Odd (m + n)) :
    (m + n).gcd (m - n) = 1 :=
  Int.isCoprime_iff_gcd_eq_one.mp (Int.isCoprime_add_sub hprime hparity)

/-- The gcd of the sum and difference of coprime integers of the same parity is two. -/
theorem Int.gcd_add_sub_eq_two {m n : ℤ} (hprime : IsCoprime m n) (hparity : Even (m + n)) :
    (m + n).gcd (m - n) = 2 := by
  refine gcd_eq_iff.mpr ⟨by grind, by grind, fun d hadd hsub ↦ ?_⟩
  have hm : d ∣ 2 * m := by grind [Int.dvd_add hadd hsub]
  have hn : d ∣ 2 * n := by grind [Int.dvd_sub hadd hsub]
  have hdvd := dvd_coe_gcd hm hn
  rw [Int.gcd_mul_left, Int.isCoprime_iff_gcd_eq_one.mp hprime] at hdvd
  simpa using hdvd

"""

count = text.count(marker)
if count != 1:
    raise SystemExit(f"expected one insertion marker, found {count}")
path.write_text(text.replace(marker, addition, 1))
