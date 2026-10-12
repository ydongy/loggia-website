#!/bin/bash
# Render design/og.html to public/og.png (1200x630) with headless Chrome.
#   scripts/export-og.sh
set -euo pipefail
cd "$(dirname "$0")/.."
chrome="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
[[ -x "$chrome" ]] || { echo "error: set CHROME to a Chrome/Chromium binary" >&2; exit 1; }
"$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1200,630 --screenshot="$PWD/public/og.png" "file://$PWD/design/og.html" > /dev/null 2>&1
file public/og.png
