#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --upgrade pip
python3 -m pip install playwright beautifulsoup4
python3 -m playwright install chromium

if command -v go >/dev/null 2>&1; then
  echo "Installing tmc/nlm via go install..."
  go install github.com/tmc/nlm@latest
else
  echo "Go not found. Please install Go first: https://go.dev/dl/"
  echo "Then run: go install github.com/tmc/nlm@latest"
fi

echo "Then run: nlm auth (or nlm auth --debug)"
