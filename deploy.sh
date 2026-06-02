#!/bin/bash
# Usage: ./deploy.sh "your commit message"
# Example: ./deploy.sh "Add new photo to Le Cafe"

MSG="${1:-Update website}"

cd "$(dirname "$0")"

git add -A
git commit -m "$MSG"
git push origin main

echo ""
echo "Pushed to GitHub. Deploy to https://arsenii.com runs automatically (Actions → Deploy to arsenii.com)."
echo "Usually live within a minute."
