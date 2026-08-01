#!/usr/bin/env bash
set -u

python3 .agent-patch.py > .agent-build.log 2>&1
status=$?
if [ "$status" -eq 0 ]; then
  lake build Mathlib.Tactic.Push.Attr Mathlib.Tactic.Push MathlibTest.Tactic.Push.Basic >> .agent-build.log 2>&1
  status=$?
fi

git config user.name "Sankalp Thakur"
git config user.email "sankalphimself@gmail.com"

if [ "$status" -eq 0 ]; then
  rm -f .agent-build.log .agent-patch.py .agent-validate.sh \
    .github/workflows/agent-apply-global-pull.yml
  git add -A
  git commit -m "feat(Tactic/Push): add a global pull attribute"
  git push origin HEAD:"${AGENT_BRANCH}"
  exit 0
fi

git reset --hard HEAD
cp /dev/null .agent-build.log
python3 .agent-patch.py >> .agent-build.log 2>&1
lake build Mathlib.Tactic.Push.Attr Mathlib.Tactic.Push MathlibTest.Tactic.Push.Basic >> .agent-build.log 2>&1
status=$?
git add .agent-build.log
git commit -m "chore: record global pull attribute build failure"
git push origin HEAD:"${AGENT_BRANCH}"
cat .agent-build.log
exit "$status"
