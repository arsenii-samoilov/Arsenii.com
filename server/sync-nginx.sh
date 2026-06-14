#!/bin/bash
# Run on the server after git pull: sync nginx config from repo and reload.
set -euo pipefail

REPO_DIR="${1:-/var/www/html}"
SNIPPETS="/etc/nginx/snippets"
SITES="/etc/nginx/sites-available/default"

cp "$REPO_DIR/server/nginx-path-redirects.conf" "$SNIPPETS/arsenii-path-redirects.conf"
cp "$REPO_DIR/server/nginx-host-canonical.conf" "$SNIPPETS/arsenii-host-canonical.conf"
cp "$REPO_DIR/server/nginx-default.conf" "$SITES"

nginx -t
systemctl reload nginx
echo "nginx reloaded"
