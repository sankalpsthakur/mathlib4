from pathlib import Path

path = Path("Mathlib/RingTheory/Int/Basic.lean")
text = path.read_text()

marker = """@[simp]
theorem isCoprime_two_right {m : ℤ} : IsCoprime m 2 ↔ Odd m := by
  simp [isCoprime_iff_nat_coprime]

"""

addition = marker + """/-- If two integers are coprime and their sum is odd, then their sum and difference are
coprime. Equivalently, the original integers have opposite parity. -/
theorem isCoprime_add_sub {m n : ℤ} (hprime : IsCoprime m n) (hparity : Odd (m + n)) :
    IsCoprime (m + n) (m - n) := by
  rw [← IsCoprime.mul_add_right_right_iff, one_mul, add_add_sub_cancel, ← two_mul]
  apply IsCoprime.mul_right
  · simpa [isCoprime_iff_nat_coprime]
  · simpa using hprime.symm.mul_add_right_left 1

"""

count = text.count(marker)
if count != 1:
    raise SystemExit(f"expected one insertion marker, found {count}")
path.write_text(text.replace(marker, addition, 1))
