#!/usr/bin/env python3
"""v0.4: un-flatten the low punctuation the v0.2 x-height scaling squashed.

v0.2 scaled every point between the baseline and y~1104 by k~0.898, so the
period, comma and low quotes came out ~10% flat (Regular period 189u tall vs
the 200u dot of '!' and Roboto's 210u). The family repair (repair_v02_zone.py)
left these alone because they are lowercase-zone punctuation.

What this does (own-weight Roboto v2.138 + family transforms, all 9 styles):
  period, comma, quotesinglbase, quotedblbase   sit on the baseline: exact
      inverse of the v0.2 scaling (y/k, snapped to Roboto) - i.e. Roboto's
      shape on Roboto's baseline, x as Sky has it.
  periodcentered, bullet, and the dots of exclamdown / questiondown   float
      at x-height-relative positions: each dot is restored to its round
      Roboto shape about its own centre, so where it sits does not move.
  colon, semicolon   are built from period/comma components and inherit the
      round dots. Their upper dot offset had never been scaled with the
      x-height (it sat 82u above the x-height in Regular); it now gets the
      same family transform as the outlines (y*k, plus the italic slant).
  ellipsis inherits the round dots.
Dashes, guillemets and math signs keep their v0.2 geometry (x-height-relative
designs, not flattened dots).

Usage: python3 restore_low_punct.py ROBOTO_DIR IN_DIR OUT_DIR
"""
import math, sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

sys.path.insert(0, str(Path(__file__).resolve().parent))
import repair_v02_zone as RZ  # noqa: E402

STYLES = RZ.STYLES
BASELINE = ["period", "comma", "quotesinglbase", "quotedblbase"]
FLOATING = {"periodcentered": None, "bullet": None, "exclamdown": "top", "questiondown": "top"}


def contours(g, glyf):
    c, e, f = g.getCoordinates(glyf)
    s = 0
    for end in e:
        yield list(range(s, end + 1))
        s = end + 1


def unflatten_floating(S, R, n, k, which):
    g = S["glyf"][n]; c, e, f = g.getCoordinates(S["glyf"])
    rc, re_, rf = R["glyf"][n].getCoordinates(R["glyf"])
    cs = list(contours(g, S["glyf"])); rcs = list(contours(R["glyf"][n], R["glyf"]))
    if which == "top":      # only the dot = the contour with the highest top
        pick = [max(range(len(cs)), key=lambda i: max(c[j][1] for j in cs[i]))]
    else:
        pick = range(len(cs))
    out = [tuple(p) for p in c]
    for i in pick:
        idx = cs[i]
        ys = [c[j][1] for j in idx]; cy = (min(ys) + max(ys)) / 2
        ridx = rcs[i] if len(rcs) == len(cs) and len(rcs[i]) == len(idx) else None
        if ridx:
            rys = [rc[j][1] for j in ridx]; rcy = (min(rys) + max(rys)) / 2
        for m, j in enumerate(idx):
            y = cy + (c[j][1] - cy) / k
            if ridx:                       # snap to Roboto's shape about the same centre
                t = cy + (rc[ridx[m]][1] - rcy)
                if abs(t - y) <= 2.5:
                    y = t
            out[j] = (c[j][0], round(y))
    g.coordinates = GlyphCoordinates(out)
    g.recalcBounds(S["glyf"])


def main():
    roboto, src, dst = map(Path, sys.argv[1:4])
    dst.mkdir(parents=True, exist_ok=True)
    for s in STYLES:
        S = TTFont(src / f"Sky-{s}.ttf"); R = TTFont(roboto / f"Roboto-{s}.ttf")
        # the v0.2 factor per style, as measured by repair_v02_zone.py
        k = {"Italic": 0.8967, "MediumItalic": 0.8967, "BoldItalic": 0.8952}.get(s, 0.8983)
        before = {n: (S["glyf"][n].yMin, S["glyf"][n].yMax) for n in BASELINE + list(FLOATING)}
        for n in BASELINE:
            RZ.unsquash(S, R, n, k)
        for n, which in FLOATING.items():
            unflatten_floating(S, R, n, k, which)
        slant = math.tan(math.radians(-S["post"].italicAngle)) if "Italic" in s else 0.0
        offs = []
        for n in ("colon", "semicolon"):
            g = S["glyf"][n]
            for comp in g.components:
                if comp.y > 400:
                    ny = round(comp.y * k)
                    comp.x = round(comp.x + (ny - comp.y) * slant)
                    offs.append(f"{n} {comp.y}->{ny}")
                    comp.y = ny
            g.recalcBounds(S["glyf"])
        for n in ("colon", "semicolon", "ellipsis"):
            S["glyf"][n].recalcBounds(S["glyf"])
        after = {n: (S["glyf"][n].yMin, S["glyf"][n].yMax) for n in before}
        S.save(dst / f"Sky-{s}.ttf")
        print(f"{s:13s} k={k} " + " ".join(f"{n}:{before[n][1]}->{after[n][1]}" for n in ("period", "comma", "quotedblbase"))
              + " | " + " ".join(offs))


if __name__ == "__main__":
    main()
