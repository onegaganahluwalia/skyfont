#!/usr/bin/env python3
"""v0.5 letter #2 — rebuild O and o from their undistorted Roboto source.

WHY (measured, see docs/design/README.md §3a):
  The v0.2 x-height scaling (y-zone 0..1082 -> 0..990) leaked into the
  capital O, and the later overshoot re-correction moved only the top of o.
  Result in v0.3 (Regular): O bottom stroke 148u vs top 164u, lower bowl
  squarer than the upper, upper-left/upper-right handles asymmetric; o top
  154u vs bottom 139u (top-heavy). Roboto's own O/o are symmetric.

WHAT:
  For each of the 9 styles, take Roboto v2.138's O/o outline (same weight,
  same point structure across all weights) and apply ONLY the documented
  family transforms, as one exact affine map per glyph:
    x' = a*x + b   so the true outline bounds land exactly on the current
                   v0.3 bounds (=> advance width, side bearings, kerning and
                   the v0.3 -12% condensing are all preserved; a ~= 0.88)
    O: y unchanged (Roboto O already sits at -20 / 1476 = locked overshoot)
    o: y' = c*y + d so the outline spans -20 .. 1007 (990 x-height + 17
       locked overshoot), i.e. the same vertical scale v0.2 intended.
  Nothing else changes: no other glyph is touched; composites (Ö, ó, …)
  inherit automatically through their component references.

Roboto source: https://github.com/googlefonts/roboto/releases/tag/v2.138
               (roboto-unhinted.zip), Apache License 2.0.

Usage: python3 scripts/glyphs/rebuild_O_o.py /path/to/roboto-unhinted [--tension T]
       --tension is for proofing alternatives only (0 = Roboto's curve).
"""
import argparse
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

ROOT = Path(__file__).resolve().parents[2]
STYLES = ["Thin", "Light", "Regular", "Medium", "Bold", "Black",
          "Italic", "MediumItalic", "BoldItalic"]
O_Y = None                 # O keeps Roboto's y (already -20 .. 1476)
o_Y = (-20.0, 1007.0)      # o: locked overshoot -20 / +17 over 990


def true_bounds(font, gname):
    gs = font.getGlyphSet()
    bp = BoundsPen(gs)
    gs[gname].draw(bp)
    return bp.bounds


def add_tension(coords, flags, ends, t):
    """Proofing aid only. For every quarter-arc on-off-off-on, slide both
    off-curve points along their own tangent toward the arc's corner (the
    intersection of the two extremum tangents) by fraction t. Tangents at
    the extrema are unchanged, so curves stay smooth; t > 0 = squarer."""
    if t == 0:
        return coords
    pts = [list(p) for p in coords]
    start = 0
    for end in ends:
        idx = list(range(start, end + 1))
        n = len(idx)
        for k in range(n):
            A, P1, P2, B = (idx[(k + j) % n] for j in range(4))
            if not (flags[A] & 1 and not flags[P1] & 1 and not flags[P2] & 1 and flags[B] & 1):
                continue
            (ax, ay), (p1x, p1y), (p2x, p2y), (bx, by) = coords[A], coords[P1], coords[P2], coords[B]
            d1 = (p1x - ax, p1y - ay)
            d2 = (p2x - bx, p2y - by)
            den = d1[0] * d2[1] - d1[1] * d2[0]
            if abs(den) < 1e-9:
                continue
            s1 = ((bx - ax) * d2[1] - (by - ay) * d2[0]) / den
            cx, cy = ax + s1 * d1[0], ay + s1 * d1[1]
            pts[P1] = [p1x + t * (cx - p1x), p1y + t * (cy - p1y)]
            pts[P2] = [p2x + t * (cx - p2x), p2y + t * (cy - p2y)]
        start = end + 1
    return [tuple(p) for p in pts]


def rebuild(sky, rob, ch, yspan, tension=0.0):
    sg = sky.getBestCmap()[ord(ch)]
    rg = rob.getBestCmap()[ord(ch)]
    sx0, sy0, sx1, sy1 = true_bounds(sky, sg)
    rx0, ry0, rx1, ry1 = true_bounds(rob, rg)
    a = (sx1 - sx0) / (rx1 - rx0)
    b = sx0 - a * rx0
    if yspan is None:
        c, d = 1.0, 0.0
    else:
        ty0, ty1 = (sy0, sy1)                # keep the current, locked extents
        c = (ty1 - ty0) / (ry1 - ry0)
        d = ty0 - c * ry0
    rglyph = rob["glyf"][rg]
    coords, ends, flags = rglyph.getCoordinates(rob["glyf"])
    flags = list(flags)
    new = [(a * x + b, c * y + d) for x, y in coords]
    new = add_tension(new, flags, list(ends), tension)
    g = sky["glyf"][sg]
    g.coordinates = GlyphCoordinates([(round(x), round(y)) for x, y in new])
    g.endPtsOfContours = list(ends)
    g.flags = bytearray(f & 0x01 for f in flags)   # on-curve bit only
    g.numberOfContours = len(ends)
    g.program = rglyph.program.__class__()
    g.program.fromBytecode(b"")
    g.recalcBounds(sky["glyf"])
    adv, _ = sky["hmtx"][sg]
    sky["hmtx"][sg] = (adv, g.xMin)
    return dict(a=round(a, 4), c=round(c, 4))


def sync_composites(font, changed):
    """Composites (Ö, ó, Ọ, …) keep their component references; only their
    cached bbox and the hmtx left side bearing (= xMin) can move by a unit."""
    glyf, hmtx = font["glyf"], font["hmtx"]
    todo = set(changed)
    grew = True
    while grew:
        grew = False
        for name in font.getGlyphOrder():
            g = glyf[name]
            if name in todo or not g.isComposite():
                continue
            if any(c.glyphName in todo for c in g.components):
                todo.add(name)
                grew = True
    for name in todo - set(changed):
        g = glyf[name]
        g.recalcBounds(glyf)
        adv, lsb = hmtx[name]
        if lsb != g.xMin:
            hmtx[name] = (adv, g.xMin)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roboto_dir")
    ap.add_argument("--tension", type=float, default=0.0)
    ap.add_argument("--out", default=str(ROOT / "fonts"))
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for s in STYLES:
        sky = TTFont(ROOT / "fonts" / f"Sky-{s}.ttf")
        rob = TTFont(Path(args.roboto_dir) / f"Roboto-{s}.ttf")
        rO = rebuild(sky, rob, "O", O_Y, args.tension)
        ro = rebuild(sky, rob, "o", o_Y, args.tension)
        sync_composites(sky, {"O", "o"})
        sky.save(out / f"Sky-{s}.ttf")
        print(f"{s:13s} O {rO}  o {ro}")


if __name__ == "__main__":
    main()
