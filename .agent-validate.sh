#!/usr/bin/env bash
set -u

old_file=Counterexamples/OrderedCancelAddCommMonoidWithBounds.lean
new_file=Counterexamples/IsOrderedCancelAddMonoidWithBounds.lean
log=.agent-build.log
: > "$log"

status=0
if ! test -f "$old_file"; then
  echo "missing source file: $old_file" >> "$log"
  status=1
elif test -e "$new_file"; then
  echo "destination already exists: $new_file" >> "$log"
  status=1
else
  mv "$old_file" "$new_file"
  cat > "$old_file" <<'LEAN'
module

public import Counterexamples.IsOrderedCancelAddMonoidWithBounds

deprecated_module "Use `Counterexamples.IsOrderedCancelAddMonoidWithBounds` instead."
  (since := "2026-08-02")
LEAN
  python3 - <<'PY' >> "$log" 2>&1
from pathlib import Path
path = Path("Counterexamples.lean")
text = path.read_text()
old = "public import Counterexamples.OrderedCancelAddCommMonoidWithBounds"
new = "public import Counterexamples.IsOrderedCancelAddMonoidWithBounds"
if text.count(old) != 1:
    raise SystemExit(f"expected one aggregate import, found {text.count(old)}")
path.write_text(text.replace(old, new))
PY
  status=$?
fi

if [ "$status" -eq 0 ]; then
  lake build Counterexamples.IsOrderedCancelAddMonoidWithBounds \
    Counterexamples.OrderedCancelAddCommMonoidWithBounds >> "$log" 2>&1
  status=$?
fi
if [ "$status" -eq 0 ]; then
  git diff --check >> "$log" 2>&1
  status=$?
fi

git config user.name "Sankalp Thakur"
git config user.email "sankalphimself@gmail.com"

if [ "$status" -eq 0 ]; then
  rm -f "$log" .agent-validate.sh \
    .github/workflows/agent-rename-ordered-counterexample.yml
  git add -A
  git commit -m "refactor(Counterexamples): rename ordered cancellation example"
  git push origin HEAD:"${AGENT_BRANCH}"
  exit 0
fi

cp "$log" /tmp/agent-build.log
git reset --hard HEAD
cp /tmp/agent-build.log "$log"
git add "$log"
git commit -m "chore: record counterexample rename build failure"
git push origin HEAD:"${AGENT_BRANCH}"
cat "$log"
exit "$status"
