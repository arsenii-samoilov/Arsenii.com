#!/bin/bash
# Git commit - add and commit (no push)
# Usage: ./commit.sh [commit message]

cd "$(dirname "$0")"
MSG="${1:-Update website}"

git add -A
git status

if git diff --staged --quiet 2>/dev/null; then
  echo "No changes to commit."
  exit 0
fi

git commit -m "$MSG"
echo "Committed. Run 'git push origin main' to push."
