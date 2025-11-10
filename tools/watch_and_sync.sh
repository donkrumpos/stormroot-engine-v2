#!/usr/bin/env bash
# Auto-sync watcher - runs in background and syncs on file changes

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WATCH_PATHS=("$REPO_ROOT/scripts" "$REPO_ROOT/data")

# Check if fswatch is available
if ! command -v fswatch &> /dev/null; then
    echo "⚠️  fswatch not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install fswatch
    else
        echo "❌ Homebrew not found. Please install fswatch manually:"
        echo "   brew install fswatch"
        exit 1
    fi
fi

echo "👀 Watching for changes in scripts/ and data/..."
echo "   Press Ctrl+C to stop"

# Watch for changes and sync
fswatch -o -r -e ".*" -i "\\.dsc$" -i "\\.yml$" "${WATCH_PATHS[@]}" | while read -r; do
    "$REPO_ROOT/tools/dev_sync.sh"
done
