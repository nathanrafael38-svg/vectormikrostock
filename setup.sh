#!/usr/bin/env bash
# Setup untuk container cloud / Linux. Windows: install Inkscape + Python, lalu pip install -r requirements.txt
set -e
pip install -r requirements.txt
command -v inkscape >/dev/null || (apt-get update -q && apt-get install -y -q inkscape ghostscript potrace)
echo "siap"
