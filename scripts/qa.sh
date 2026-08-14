#!/usr/bin/env bash
# Sky font QA script — runs fontbakery's universal check suite against every
# shipped font file. Requires: pip install fontbakery --break-system-packages
#
# Usage: ./scripts/qa.sh

set -e

FONTS_DIR="$(dirname "$0")/../fonts"

if ! command -v fontbakery &> /dev/null; then
    echo "fontbakery not found. Install it with:"
    echo "  pip install fontbakery --break-system-packages"
    exit 1
fi

if [ ! -d "$FONTS_DIR" ]; then
    echo "Fonts directory not found at $FONTS_DIR"
    exit 1
fi

echo "Running fontbakery against all fonts in $FONTS_DIR ..."
echo ""

FAIL_COUNT=0
for font in "$FONTS_DIR"/*.ttf; do
    echo "=== $(basename "$font") ==="
    fontbakery check-universal "$font" --loglevel WARN || FAIL_COUNT=$((FAIL_COUNT+1))
    echo ""
done

echo "--------------------------------------------"
if [ "$FAIL_COUNT" -eq 0 ]; then
    echo "All fonts checked clean (or warnings only)."
else
    echo "$FAIL_COUNT font(s) have FAIL-level issues. Review output above."
    echo "Note: not every FAIL is fatal — fontbakery includes some legacy/"
    echo "opinionated checks (e.g. Mac platform name table entries) that many"
    echo "shipped, widely-used fonts also fail. Use judgment; prioritize issues"
    echo "that affect actual rendering (vertical metrics, missing glyphs,"
    echo "malformed tables) over stylistic/legacy warnings."
fi
