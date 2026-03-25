#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="TextEditMac"
SRC="${SCRIPT_DIR}/dist/${APP_NAME}.app"
DST="/Applications/${APP_NAME}.app"

if [ ! -d "$SRC" ]; then
    echo "Error: ${SRC} not found. Run build_app.sh first." >&2
    exit 1
fi

echo "Installing ${APP_NAME} to /Applications..."

if [ -d "$DST" ]; then
    echo "Removing old version..."
    rm -rf "$DST"
fi

cp -R "$SRC" "$DST"

echo "Re-signing after copy..."
codesign --force --deep --sign - "$DST"
codesign --verify --verbose "$DST" 2>&1 || true

echo ""
echo "Installed: ${DST}"
echo "Run: open /Applications/${APP_NAME}.app"
