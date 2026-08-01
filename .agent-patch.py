from pathlib import Path

path = Path("Mathlib/Analysis/Calculus/ContDiff/Operations.lean")
text = path.read_text()

start_marker = "-- TODO: generalize to `f g : E → 𝕜'`"
end_marker = "\nend AlgebraInverse"
start = text.find(start_marker)
if start < 0:
    raise SystemExit("could not find the division generalization TODO")
end = text.find(end_marker, start)
if end < 0:
    raise SystemExit("could not find the end of the algebra-inverse section")

block = text[start:end]
if block.count("{f g : E → 𝕜}") != 4:
    raise SystemExit(
        f"expected four scalar-valued division declarations, found {block.count('{f g : E → 𝕜}')}"
    )
block = block.replace(start_marker + "\n", "", 1)
block = block.replace("{f g : E → 𝕜}", "{f g : E → 𝕜'}")
path.write_text(text[:start] + block + text[end:])
