#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install --upgrade pip
python3 -m pip install playwright beautifulsoup4
python3 -m playwright install chromium

echo "Done. Try: python3 scripts/url_to_pdf.py --url '<URL>' --out /tmp/page.pdf"
