#!/bin/bash
# Copy latest resume PDF from Desktop, commit, push — GitHub Actions deploys to arsenii.com.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="/Users/arsenii/Desktop/Desktop/Arsenii Resume/Arsenii Samoilov Resume.pdf"
DEST="$ROOT/documents/Arsenii Samoilov.pdf"

if [[ ! -f "$SRC" ]]; then
  echo "Resume not found: $SRC" >&2
  exit 1
fi

cp "$SRC" "$DEST"
echo "Copied resume to documents/Arsenii Samoilov.pdf"

"$ROOT/deploy.sh" "Resume: sync latest PDF"
