#!/usr/bin/env bash
# Simple polling-based watcher (no external dependencies)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$REPO_ROOT/scripts"
DATA_DIR="$REPO_ROOT/data"
LAST_SYNC=0

echo "👀 Watching scripts/ and data/ for changes..."
echo "   (Checking every 2 seconds)"
echo "   Press Ctrl+C to stop"
echo ""

while true; do
    # Get the most recent modification time
    LATEST=$(find "$SCRIPTS_DIR" "$DATA_DIR" -type f \( -name "*.dsc" -o -name "*.yml" \) -exec stat -f "%m" {} \; 2>/dev/null | sort -n | tail -1)
    
    if [ -n "$LATEST" ] && [ "$LATEST" -gt "$LAST_SYNC" ]; then
        "$REPO_ROOT/tools/dev_sync.sh"
        LAST_SYNC=$(date +%s)
    fi
    
    sleep 2
done
