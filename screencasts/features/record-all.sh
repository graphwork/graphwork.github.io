#!/usr/bin/env bash
# Record all feature screenshots using VHS.
# Usage: ./screencasts/features/record-all.sh
# Outputs: screencasts/features/*.png → copied to public/features/*.png
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_DIR"

# Check dependencies
for cmd in vhs ttyd ffmpeg wg; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "Error: '$cmd' not found." >&2
    exit 1
  fi
done

# Setup demo project (once)
echo "Setting up demo project..."
WG_AGENT_ID= bash screencasts/features/setup-features-demo.sh /tmp/wg-features-demo

TAPES=(
  dashboard
  graph-explorer
  inspector
  agents
  cycles
  evaluation
  chat
)

mkdir -p public/features

for tape in "${TAPES[@]}"; do
  echo ""
  echo "Recording: $tape"
  vhs "screencasts/features/${tape}.tape" || {
    echo "Warning: Failed to record $tape, skipping"
    continue
  }
  if [ -f "screencasts/features/${tape}.png" ]; then
    cp "screencasts/features/${tape}.png" "public/features/${tape}.png"
    echo "  → public/features/${tape}.png"
  fi
done

echo ""
echo "Done! Screenshots in public/features/:"
ls -lh public/features/*.png 2>/dev/null || echo "(no screenshots produced)"
