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

TENSION (v0.5 spec change approved by Gagan, 18 Nov 2026 — option B):
  O/o are drawn squarer than Roboto (Helvetica-leaning). Uprights use
  t = 0.12; each italic uses the t that gives its deslanted outer contour
  the same squareness as its upright partner (scripts/glyphs/o_tension.json).

Usage: python3 scripts/glyphs/rebuild_O_o.py /path/to/roboto-unhinted
           [--in DIR] [--out DIR] [--tension T] [--tension-json FILE]
"""
import argparse
import json
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
    """Squarer curve ("tension"), affine-invariant so it works identically on
    upright and slanted outlines. For every arc on-off(1..n)-on, find the
    arc's corner (intersection of the tangents at its two on-curve ends,
    i.e. the extremum tangents) and slide every off-curve point toward that
    corner by fraction t. End tangents are unchanged, so curves stay smooth
    and extrema stay extrema; t > 0 = squarer, t = 0 = Roboto's curve.
    Handles Roboto's upright quarters (2 off-curves) and italic quarters
    (2-3 off-curves with implied on-curves)."""
    if t == 0:
        return coords
    pts = [list(p) for p in coords]
    start = 0
    for end in ends:
        idx = list(range(start, end + 1))
        n = len(idx)
        ons = [k for k in range(n) if flags[idx[k]] & 1]
        for j, k0 in enumerate(ons):
            k1 = ons[(j + 1) % len(ons)]
            span = (k1 - k0) % n or n
            offs = [idx[(k0 + m) % n] for m in range(1, span)]
            if not offs:
                continue
            A, B = idx[k0], idx[k1]
            (ax, ay), (bx, by) = coords[A], coords[B]
            d1 = (coords[offs[0]][0] - ax, coords[offs[0]][1] - ay)
            d2 = (coords[offs[-1]][0] - bx, coords[offs[-1]][1] - by)
            den = d1[0] * d2[1] - d1[1] * d2[0]
            if abs(den) < 1e-9:
                continue
            s1 = ((bx - ax) * d2[1] - (by - ay) * d2[0]) / den
            s2 = ((bx - ax) * d1[1] - (by - ay) * d1[0]) / den
            if s1 <= 0 or s2 <= 0:      # not a convex corner arc
                continue
            cx, cy = ax + s1 * d1[0], ay + s1 * d1[1]
            for P in offs:
                px, py = coords[P]
                pts[P] = [px + t * (cx - px), py + t * (cy - py)]
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
    ap.add_argument("--tension", type=float, default=0.0,
                    help="tension for all styles (overridden by --tension-json)")
    ap.add_argument("--tension-json",
                    help='per style/glyph tension, e.g. {"Italic": {"O": 0.13, "o": 0.12}}')
    ap.add_argument("--in", dest="indir", default=str(ROOT / "fonts"))
    ap.add_argument("--out", default=str(ROOT / "fonts"))
    args = ap.parse_args()
    tj = json.load(open(args.tension_json)) if args.tension_json else {}
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for s in STYLES:
        sky = TTFont(Path(args.indir) / f"Sky-{s}.ttf")
        rob = TTFont(Path(args.roboto_dir) / f"Roboto-{s}.ttf")
        tO = tj.get(s, {}).get("O", args.tension)
        to = tj.get(s, {}).get("o", args.tension)
        rO = rebuild(sky, rob, "O", O_Y, tO)
        ro = rebuild(sky, rob, "o", o_Y, to)
        sync_composites(sky, {"O", "o"})
        sky.save(out / f"Sky-{s}.ttf")
        print(f"{s:13s} O {rO} t={tO}  o {ro} t={to}")


if __name__ == "__main__":
    main()
