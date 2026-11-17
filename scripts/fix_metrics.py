#!/usr/bin/env python3
"""v0.5 metrics fixes, applied to all 9 styles.

1. Left side bearings: set hmtx lsb = glyf xMin for every glyph.
   v0.3 shipped ~1,360 glyphs per font (almost all composites: accented
   letters) whose hmtx lsb disagreed with the outline's xMin by 2-18u.
   The outlines themselves are already where they should be (Chrome and
   FreeType, unhinted, draw them from glyf coordinates — verified), so this
   is a metrics-consistency fix: hmtx lsb is what the TrueType phantom
   points, hinting and hmtx-based layout/PDF tools use, and validators flag
   the mismatch. Advance widths are not changed.

2. Italic angle (italic styles only): set post.italicAngle and the hhea
   caret slope to the slant MEASURED from the straight stems of
   I, l, H, T, E, L, F, h, d, b (median over all straight stem segments; one value for all three
   italics, the median of their per-style measurements).
   v0.3 declared -12 deg (Roboto's nominal value) with caret 100/21
   (11.9 deg), but Sky's italic stems lean 8.66 deg: Roboto's true stem
   slant is 9.86 deg and Sky's -12% horizontal condensing reduces it to
   atan(0.88 * tan 9.86 deg).

Usage: python3 scripts/fix_metrics.py IN_DIR OUT_DIR
"""
import math, statistics, sys
from pathlib import Path
from fontTools.ttLib import TTFont

STYLES = ["Thin", "Light", "Regular", "Medium", "Bold", "Black",
          "Italic", "MediumItalic", "BoldItalic"]
STEM_GLYPHS = ["I", "l", "H", "T", "E", "L", "F", "h", "d", "b"]


def measured_slant(font):
    glyf = font["glyf"]
    angs = []
    for n in STEM_GLYPHS:
        c, ends, flags = glyf[n].getCoordinates(glyf)
        s = 0
        for e in ends:
            idx = list(range(s, e + 1))
            for k, i in enumerate(idx):
                j = idx[(k + 1) % len(idx)]
                if flags[i] & 1 and flags[j] & 1:
                    (x1, y1), (x2, y2) = c[i], c[j]
                    if abs(y2 - y1) > 400:
                        a = math.degrees(math.atan((x2 - x1) / (y2 - y1)))
                        if 3 < a < 15:
                            angs.append(a)
            s = e + 1
    return statistics.median(angs), len(angs)


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    per_style = {s: measured_slant(TTFont(src / f"Sky-{s}.ttf"))[0]
                 for s in STYLES if "Italic" in s}
    family = round(statistics.median(per_style.values()), 2)   # one value for the family
    print("measured italic slant:", {k: round(v, 3) for k, v in per_style.items()}, "-> family", family)
    for s in STYLES:
        f = TTFont(src / f"Sky-{s}.ttf")
        glyf, hmtx = f["glyf"], f["hmtx"]
        fixed = comp = 0
        for n in f.getGlyphOrder():
            g = glyf[n]
            g.recalcBounds(glyf)
            if g.numberOfContours == 0:
                continue
            adv, lsb = hmtx[n]
            if lsb != g.xMin:
                hmtx[n] = (adv, g.xMin)
                fixed += 1
                comp += g.isComposite()
        msg = f"{s:13s} lsb fixed {fixed} ({comp} composite, {fixed - comp} simple)"
        if "Italic" in s:
            _, cnt = measured_slant(f)
            ang = family
            old = (f["post"].italicAngle, f["hhea"].caretSlopeRise, f["hhea"].caretSlopeRun)
            f["post"].italicAngle = -ang
            f["hhea"].caretSlopeRise = 2048
            f["hhea"].caretSlopeRun = round(2048 * math.tan(math.radians(ang)))
            msg += (f" | italicAngle {old[0]} -> {-ang} (from {cnt} stem segments);"
                    f" caret {old[1]}/{old[2]} -> 2048/{f['hhea'].caretSlopeRun}")
        f.save(dst / f"Sky-{s}.ttf")
        print(msg)


if __name__ == "__main__":
    main()
