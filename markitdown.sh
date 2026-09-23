#!/bin/bash
# Wrapper script for markitdown
# Usage: ./markitdown.sh <input-file> [options]
# Example: ./markitdown.sh file.pdf -o output.md

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_BIN="$SCRIPT_DIR/.venv/bin/markitdown"

if [ ! -f "$VENV_BIN" ]; then
    echo "❌ Không tìm thấy markitdown trong venv!"
    echo "   Chạy: pip install 'markitdown[all]' trong venv"
    exit 1
fi

exec "$VENV_BIN" "$@"
