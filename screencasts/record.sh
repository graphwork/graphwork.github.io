#!/usr/bin/env bash
# Record the workgraph TUI demo screencast.
# Usage: ./screencasts/record.sh
#
# Prerequisites:
#   - vhs (https://github.com/charmbracelet/vhs) — `go install github.com/charmbracelet/vhs@latest`
#     or download from https://github.com/charmbracelet/vhs/releases
#   - ttyd — `brew install ttyd` or download from https://github.com/tsl0922/ttyd/releases
#   - ffmpeg — `apt install ffmpeg` or `brew install ffmpeg`
#   - wg (workgraph) — `cargo install --path /path/to/workgraph`
#
# Outputs:
#   screencasts/demo.gif
#   screencasts/demo.webm

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check dependencies
for cmd in vhs ttyd ffmpeg wg; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "Error: '$cmd' not found. See comments in this script for install instructions." >&2
    exit 1
  fi
done

echo "Recording TUI screencast..."
cd "$REPO_DIR"
vhs screencasts/demo.tape

echo ""
echo "Done! Outputs:"
ls -lh screencasts/demo.gif screencasts/demo.webm
