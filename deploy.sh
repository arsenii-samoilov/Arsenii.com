#!/bin/bash
# Deploy to git - add, commit, push
# Usage: ./deploy.sh [commit message]

cd "$(dirname "$0")"
MSG="${1:-Deploy website updates}"

git add -A
git status

if git diff --staged --quiet 2>/dev/null; then
  echo "No changes to commit."
  exit 0
fi

git commit -m "$MSG"
git push origin main

echo "Deployed to origin/main"
