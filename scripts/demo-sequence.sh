#!/usr/bin/env bash
# demo-sequence.sh — the actual commands shown in the demo recording
# Called by record-demo.sh inside asciinema rec --command
# 5 scenes, ~35 seconds total

set -e

# Activate venv silently
source /Users/nameetpotnis/Projects/pdfmux/.venv/bin/activate 2>/dev/null
cd /Users/nameetpotnis/Projects/pdfmux

# Clean up any previous output files
rm -f demo-sample.md demo-sample.chunks.json demo-sample.json

# Typing simulator — realistic 60-90ms between keystrokes
type_cmd() {
  local cmd="$1"
  for (( i=0; i<${#cmd}; i++ )); do
    printf '%s' "${cmd:$i:1}"
    # Vary delay: 50-100ms range
    sleep 0.$(printf '%02d' $(( RANDOM % 50 + 50 )))
  done
}

prompt() {
  printf '\033[1;32m$\033[0m '
}

# === Scene 1: Basic extraction (the hook) ===
sleep 0.6
prompt
type_cmd "pdfmux convert demo-sample.pdf"
echo
sleep 0.3
pdfmux convert demo-sample.pdf
sleep 2.0

# === Scene 2: Doctor command (show the ecosystem) ===
prompt
type_cmd "pdfmux doctor"
echo
sleep 0.3
pdfmux doctor
sleep 2.5

# === Scene 3: RAG chunking (the killer feature) ===
prompt
type_cmd "pdfmux convert demo-sample.pdf --chunk --max-tokens 500"
echo
sleep 0.3
pdfmux convert demo-sample.pdf --chunk --max-tokens 500
sleep 2.0

# === Scene 4: Cost-aware mode ===
prompt
type_cmd "pdfmux convert demo-sample.pdf --mode economy"
echo
sleep 0.3
pdfmux convert demo-sample.pdf --mode economy
sleep 1.5

# === Scene 5: Schema extraction ===
prompt
type_cmd "pdfmux convert demo-sample.pdf --schema paper"
echo
sleep 0.3
pdfmux convert demo-sample.pdf --schema paper
sleep 1.5

echo
