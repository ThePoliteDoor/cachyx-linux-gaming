#!/usr/bin/env bash
set -e

./build.sh
python3 -m src.main "/"

cd docs || exit 1

# Start server in background
python3 -m http.server 8888 &
SERVER_PID=$!

# Ensure server stops if script exits for ANY reason
cleanup() {
    kill "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT

# Give server time to start
sleep 1

# Use a temporary Brave profile so --wait actually blocks
TMP_PROFILE=$(mktemp -d)

brave \
  --user-data-dir="$TMP_PROFILE" \
  --new-window \
  --wait \
  http://localhost:8888

# Cleanup temp profile after browser closes
rm -rf "$TMP_PROFILE"
