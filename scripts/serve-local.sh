#!/usr/bin/env bash
# Local preview for growth briefs. From repo root: ./scripts/serve-local.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PORT="${PORT:-8765}"
echo "Serving $ROOT at http://127.0.0.1:$PORT/"
echo "QA hub: http://127.0.0.1:$PORT/qa-briefs.html"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
