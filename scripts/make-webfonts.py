#!/usr/bin/env python3
"""Regenerate the website's web fonts from the shipped TTFs.

Copies fonts/*.ttf (+ LICENSE/NOTICE) -> website/fonts/ (download links) and compresses
each to website/fonts/*.woff2 (what the page actually loads). Run after any
change to fonts/ so the site never drifts from the release files.

Requires: pip install fonttools brotli
Usage:    python3 scripts/make-webfonts.py
"""
import hashlib
import shutil
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "fonts"
DST = ROOT / "website" / "fonts"
STYLES = ["Thin", "Light", "Regular", "Medium", "Bold", "Black",
          "Italic", "MediumItalic", "BoldItalic"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    # Apache 2.0 requires LICENSE + NOTICE to travel with redistributed files.
    for doc in ("LICENSE.txt", "NOTICE.txt"):
        shutil.copy2(SRC / doc, DST / doc)
    for style in STYLES:
        ttf = SRC / f"Sky-{style}.ttf"
        out_ttf = DST / ttf.name
        if not out_ttf.exists() or sha(out_ttf) != sha(ttf):
            shutil.copy2(ttf, out_ttf)
        font = TTFont(ttf)
        font.flavor = "woff2"
        out = DST / f"Sky-{style}.woff2"
        font.save(out)
        print(f"{style:13s} ttf {ttf.stat().st_size/1024:6.0f} KB  sha {sha(ttf)}"
              f"  ->  woff2 {out.stat().st_size/1024:5.0f} KB")


if __name__ == "__main__":
    main()
