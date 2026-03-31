#!/usr/bin/env bash
# record-demo.sh — scripted terminal demo for pdfmux README
# Uses asciinema + svg-term-cli for a clean, repeatable recording.
#
# Usage:
#   cd /Users/nameetpotnis/Projects/pdfmux
#   bash scripts/record-demo.sh
#
# Output: demo.cast → demo.svg

set -e

PROJ="/Users/nameetpotnis/Projects/pdfmux"
CAST_FILE="$PROJ/demo.cast"
SVG_FILE="$PROJ/demo.svg"

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

echo "Recording to $CAST_FILE ..."

asciinema rec \
  --overwrite \
  --cols 80 \
  --rows 24 \
  --title "pdfmux — PDF extraction that checks its own work" \
  --command "bash $PROJ/scripts/demo-sequence.sh" \
  "$CAST_FILE"

echo ""
echo "Recorded: $CAST_FILE"
echo ""
echo "Converting to SVG ..."

npx svg-term-cli \
  --in "$CAST_FILE" \
  --out "$SVG_FILE" \
  --window \
  --no-cursor \
  --width 80 \
  --height 24

echo "Done: $SVG_FILE"
