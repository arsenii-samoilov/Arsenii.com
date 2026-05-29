#!/bin/bash
# Run from arsenii-website folder to commit and push all changes

cd "$(dirname "$0")"

if [ -z "$(git status --porcelain)" ]; then
  echo "Nothing to commit — site is up to date."
  exit 0
fi

echo "Changed files:"
git status --short

echo ""
read -p "Commit message (or press Enter for auto): " MSG

if [ -z "$MSG" ]; then
  MSG="Update site — $(date '+%Y-%m-%d %H:%M')"
fi

git add -A
git commit -m "$MSG"
git push origin main

echo ""
echo "Done. Server will pull within 30 minutes."
