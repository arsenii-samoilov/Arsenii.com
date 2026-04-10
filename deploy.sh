#!/bin/bash
# Usage: ./deploy.sh "your commit message"
# Example: ./deploy.sh "Add new photo to Le Cafe"

MSG="${1:-Update website}"

cd "$(dirname "$0")"

git add -A
git commit -m "$MSG"
git push origin main

echo ""
echo "Done! Live at: https://github.com/arsenii-samoilov/Arsenii.com"
