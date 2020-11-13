#!/bin/bash

set -euo pipefail

if [ "$(uname -n)" != "arsenii-dot-com" ]; then
  echo "Incorrect nodename. Are you sure you're in the right place?"
  exit 1
fi

if [[ $USER != "hal" ]]; then
  echo "I'm afraid I can't let you do that, Dave..."
  echo ""
  echo "Make sure you're logged in as hal."
  exit 1
fi

echo "Cloning repo..."
echo ""

git checkout v2
git pull

export NODE_ENV=production

npm install
npm run build:prod

echo "Restarting PM2..."
echo ""

pm2 stop arsenii > /dev/null 2>&1
pm2 start bin/www --name arsenii

echo "PM2 restarted."
echo ""
echo "Done."