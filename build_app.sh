#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

APP_NAME="TextEditMac"
APP_PATH="dist/${APP_NAME}.app"

echo "=== Building ${APP_NAME}.app ==="

rm -rf build dist

echo "[1/4] Running PyInstaller..."
python3 -m PyInstaller ${APP_NAME}.spec --noconfirm

if [ ! -d "$APP_PATH" ]; then
    echo "Build failed!" >&2
    exit 1
fi

echo "[2/4] Placing qt.conf in Resources..."
cp resources/qt.conf "${APP_PATH}/Contents/Resources/qt.conf"

echo "[3/4] Deep codesigning the app bundle..."
codesign --force --deep --sign - "$APP_PATH"

echo "[4/4] Verifying codesign..."
codesign --verify --verbose "$APP_PATH" 2>&1 || true

echo ""
echo "=== Build successful ==="
echo "App location: ${APP_PATH}"
echo "Size: $(du -sh "$APP_PATH" | cut -f1)"
echo ""
echo "To install to /Applications, run:"
echo "  ./install.sh"
echo ""
echo "Or run directly:"
echo "  open ${APP_PATH}"
