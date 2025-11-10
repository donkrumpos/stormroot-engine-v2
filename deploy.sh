#!/usr/bin/env bash
set -euo pipefail

# --- locate repo root (dir of this script) ---
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# === Config ===
REMOTE_HOST="stormroot"
REMOTE_DENIZEN="/home/minecraft/server/plugins/Denizen"

LOCAL_SCRIPTS_DIR="${REPO_DIR}/scripts"
LOCAL_DATA_DIR="${REPO_DIR}/data"

RELOAD_MODE="${RELOAD_MODE:-}"   # tmux|screen|rcon|""
TMUX_SESSION="${TMUX_SESSION:-mc}"
SCREEN_NAME="${SCREEN_NAME:-mc}"
RCON_BIN="${RCON_BIN:-/usr/bin/rcon-cli}"
RCON_PASS="${RCON_PASS:-}"

DRY_RUN=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN="--dry-run"
  echo "🔎 Dry run: no remote changes will be made."
fi

# --- sanity checks (clear errors fast) ---
echo "📍 Repo: ${REPO_DIR}"
if [[ ! -d "$LOCAL_SCRIPTS_DIR" ]]; then
  echo "❌ Missing local scripts dir: $LOCAL_SCRIPTS_DIR"
  echo "   Make sure your repo has a 'scripts/' folder."
  exit 1
fi
if [[ ! -d "$LOCAL_DATA_DIR" ]]; then
  echo "❌ Missing local data dir: $LOCAL_DATA_DIR"
  echo "   Make sure your repo has a 'data/' folder."
  exit 1
fi

echo "🔐 Checking SSH to ${REMOTE_HOST}…"
ssh -o BatchMode=yes "${REMOTE_HOST}" true 2>/dev/null || {
  echo "❌ Could not SSH to '${REMOTE_HOST}'. Check ~/.ssh/config alias/key."
  exit 1
}

echo "📁 Ensuring remote directories exist…"
ssh "${REMOTE_HOST}" "mkdir -p '${REMOTE_DENIZEN}/scripts' '${REMOTE_DENIZEN}/data'"

echo "🚚 Syncing scripts → ${REMOTE_HOST}:${REMOTE_DENIZEN}/scripts ..."
rsync -az ${DRY_RUN} --delete \
  --chmod=Du=rwx,Fu=rw,Do=rx,Fo=r \
  --exclude='**/*.dsc.OFF' \
  "${LOCAL_SCRIPTS_DIR}/" "${REMOTE_HOST}:${REMOTE_DENIZEN}/scripts/"

echo "🚚 Syncing data → ${REMOTE_HOST}:${REMOTE_DENIZEN}/data ..."
rsync -az ${DRY_RUN} --delete \
  --chmod=Du=rwx,Fu=rw,Do=rx,Fo=r \
  "${LOCAL_DATA_DIR}/" "${REMOTE_HOST}:${REMOTE_DENIZEN}/data/"

# --- optional reload ---
case "$RELOAD_MODE" in
  tmux)
    echo "🔁 Reloading via tmux (${TMUX_SESSION})…"
    ssh "${REMOTE_HOST}" "tmux send-keys -t '${TMUX_SESSION}' 'denizen reload' Enter"
    ;;
  screen)
    echo "🔁 Reloading via screen (${SCREEN_NAME})…"
    ssh "${REMOTE_HOST}" "screen -S '${SCREEN_NAME}' -p 0 -X stuff 'denizen reload^M'"
    ;;
  rcon)
    if [[ -n "$RCON_PASS" ]]; then
      echo "🔁 Reloading via rcon…"
      ssh "${REMOTE_HOST}" "${RCON_BIN} -p '${RCON_PASS}' 'denizen reload'"
    else
      echo "ℹ️  RELOAD_MODE=rcon but RCON_PASS empty; skipping reload."
    fi
    ;;
  "" ) echo "ℹ️  Reload skipped (set RELOAD_MODE to enable).";;
  *  ) echo "⚠️  Unknown RELOAD_MODE='${RELOAD_MODE}'; skipping reload.";;
esac

echo "✅ Deployment complete."