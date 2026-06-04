#!/usr/bin/env bash
# Local preview for growth briefs. From repo root: ./scripts/serve-local.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PORT="${PORT:-8765}"
BASE="http://localhost:${PORT}"

if lsof -nP -iTCP:"${PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Preview server already on ${BASE}"
  echo "Example: ${BASE}/10adventures/index.html"
  exit 0
fi

echo "Starting preview server on ${BASE} (Ctrl+C to stop)"
echo "QA hub: ${BASE}/qa-briefs-wave2.html"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
