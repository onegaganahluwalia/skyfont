#!/usr/bin/env python3
"""Stamp release metadata on all 9 fonts.

- head.fontRevision and name ID 5 ("Version X.YYY") = the Sky release
  (the files still carried Roboto's 2.138 until v0.4)
- name ID 3 (unique ID) = "Sky:<PostScript name>:<version>"
- OS/2.xAvgCharWidth recalculated from the actual advance widths (it was
  stale: 1168 vs 997 in Regular, from before the v0.3 condensing)

Usage: python3 scripts/set_release.py VERSION IN_DIR OUT_DIR   (e.g. 0.4.0)
"""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont

STYLES = ["Thin", "Light", "Regular", "Medium", "Bold", "Black",
          "Italic", "MediumItalic", "BoldItalic"]


def main():
    ver, src, dst = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    parts = [int(x) for x in (ver.split(".") + ["0", "0"])[:3]]
    rev_str = f"{parts[0]}.{parts[1]}{parts[2]:02d}"      # 0.4.0 -> 0.400
    rev = float(rev_str)
    dst.mkdir(parents=True, exist_ok=True)
    for s in STYLES:
        f = TTFont(src / f"Sky-{s}.ttf")
        old = (f["head"].fontRevision, f["OS/2"].xAvgCharWidth)
        f["head"].fontRevision = rev
        ps = f["name"].getDebugName(6)
        for rec in f["name"].names:
            if rec.nameID == 5:
                rec.string = f"Version {rev_str}"
            elif rec.nameID == 3:
                rec.string = f"Sky:{ps}:{rev_str}"
        f["OS/2"].recalcAvgCharWidth(f)
        f.save(dst / f"Sky-{s}.ttf")
        print(f"{s:13s} fontRevision {old[0]:.3f} -> {rev_str}; xAvgCharWidth {old[1]} -> {f['OS/2'].xAvgCharWidth}")


if __name__ == "__main__":
    main()
