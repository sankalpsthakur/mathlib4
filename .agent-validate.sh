#!/usr/bin/env bash
set -u

python3 .agent-patch.py > .agent-build.log 2>&1
status=$?
if [ "$status" -eq 0 ]; then
  lake build Mathlib.Analysis.Calculus.ContDiff.Operations >> .agent-build.log 2>&1
  status=$?
fi

git config user.name "Sankalp Thakur"
git config user.email "sankalphimself@gmail.com"

if [ "$status" -eq 0 ]; then
  rm -f .agent-build.log .agent-patch.py .agent-validate.sh
  git add -A
  git commit -m "feat(ContDiff): generalize division to field extensions"
  git push origin HEAD:"${AGENT_BRANCH}"
  exit 0
fi

cp .agent-build.log /tmp/agent-build.log
git reset --hard HEAD
cp /tmp/agent-build.log .agent-build.log
git add .agent-build.log
git commit -m "chore: record ContDiff division build failure"
git push origin HEAD:"${AGENT_BRANCH}"
cat .agent-build.log
exit "$status"
