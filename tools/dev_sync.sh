#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_SCRIPTS="$REPO_ROOT/scripts"
SRC_DATA="$REPO_ROOT/data"

DST_DENIZEN="$REPO_ROOT/_server_local/plugins/Denizen"
DST_SCRIPTS="$DST_DENIZEN/scripts"
DST_DATA="$DST_DENIZEN/data"

mkdir -p "$DST_SCRIPTS" "$DST_DATA"

rsync -a --delete "$SRC_SCRIPTS/" "$DST_SCRIPTS/" 2>&1 | grep -v "^$" || true
rsync -a --delete "$SRC_DATA/"    "$DST_DATA/"    2>&1 | grep -v "^$" || true

echo "✅ Synced at $(date '+%H:%M:%S')"