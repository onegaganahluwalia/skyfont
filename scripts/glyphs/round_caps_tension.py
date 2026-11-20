#!/usr/bin/env python3
"""v0.4: give C, G, Q, D, Ø, Œ the approved squarer O curve (all 9 styles).

Spec change approved by Gagan (18 Nov 2026): round letters inherit the O/o
curve DNA (rebuild_O_o.py; t from o_tension.json, the O value per style).

  C, G, D, Œ  the same tension operator as O, applied to every curve arc of
              the current (repaired) outline: each off-curve point slides
              toward the arc's tangent-intersection corner by t. On-curve
              points, extrema, stroke weights at 12/3/6/9 o'clock, terminals'
              cut angles, straight segments and corner-softening chamfers do
              not move.
  Q, Ø        the bowl IS the O: these glyphs are rebuilt as the new O
              (aligned to the glyph's own bowl position) united with the
              glyph's own extra part: Q's tail, and Ø's slash re-formed as the
              strip between its two straight edges cut at the glyph's own top
              and bottom, so it runs unbroken through the squarer counter.
Advance widths, side bearings (lsb := xMin), overshoots and kerning unchanged.

Usage: python3 round_caps_tension.py ROBOTO_DIR IN_DIR OUT_DIR
"""
import json, math, sys
from pathlib import Path
import pathops
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rebuild_O_o as RB  # noqa: E402

STYLES = ["Thin", "Light", "Regular", "Medium", "Bold", "Black",
          "Italic", "MediumItalic", "BoldItalic"]
TENSION = json.load(open(Path(__file__).resolve().parent / "o_tension.json"))
DIRECT = ["C", "G", "D", "OE"]
BOWL = ["Q", "Oslash"]


def path_of(font, n, dx=0):
    p = pathops.Path(); gs = font.getGlyphSet()
    gs[n].draw(TransformPen(p.getPen(), (1, 0, 0, 1, dx, 0)))
    return p


def op(a, b, o):
    return pathops.op(a, b, o, fix_winding=True, keep_starting_points=False)


def tension_direct(font, n, t):
    g = font["glyf"][n]
    c, e, f = g.getCoordinates(font["glyf"])
    new = RB.add_tension(list(c), list(f), list(e), t)
    from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
    g.coordinates = GlyphCoordinates([(round(x), round(y)) for x, y in new])
    g.recalcBounds(font["glyf"])


def best_dx(G, O0font):
    best = None
    for rng in (range(-200, 201, 4), None):
        if rng is None:
            rng = range(best[0] - 4, best[0] + 5)
        for dx in rng:
            x = abs(op(G, path_of(O0font, "O", dx), pathops.PathOp.XOR).area)
            if best is None or x < best[1]:
                best = (dx, x)
    return best[0]


def dilate(p, r):
    q = pathops.Path(); q.addPath(p)
    q.stroke(2 * r, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    q.convertConicsToQuads()
    return op(p, q, pathops.PathOp.UNION)


def slash_band(font, n):
    """Strip between the two longest straight edges of the glyph (the slash)."""
    g = font["glyf"][n]
    c, e, f = g.getCoordinates(font["glyf"])
    segs = []
    s0 = 0
    for end in e:
        idx = list(range(s0, end + 1))
        for k, i in enumerate(idx):
            j = idx[(k + 1) % len(idx)]
            if f[i] & 1 and f[j] & 1:
                (x1, y1), (x2, y2) = c[i], c[j]
                L = math.hypot(x2 - x1, y2 - y1)
                if abs(y2 - y1) > 0.3 * L:          # slanted, not a bar
                    segs.append((L, (x1, y1), (x2, y2)))
        s0 = end + 1
    segs.sort(reverse=True)
    (l1, a1, b1) = segs[0]
    # second edge: longest segment not collinear with the first
    def dist(p, a, b):
        return abs((b[0]-a[0])*(a[1]-p[1]) - (a[0]-p[0])*(b[1]-a[1])) / math.hypot(b[0]-a[0], b[1]-a[1])
    a2, b2 = next((a, b) for _, a, b in segs[1:] if dist(a, a1, b1) > 20)
    def ext(a, b, T=4000):
        d = (b[0]-a[0], b[1]-a[1]); L = math.hypot(*d); d = (d[0]/L, d[1]/L)
        return (a[0]-T*d[0], a[1]-T*d[1]), (a[0]+T*d[0], a[1]+T*d[1])
    p1, q1 = ext(a1, b1)
    p2, q2 = ext(a2, b2)
    if (q1[0]-p1[0])*(q2[0]-p2[0]) + (q1[1]-p1[1])*(q2[1]-p2[1]) < 0:
        p2, q2 = q2, p2
    band = pathops.Path(); pen = band.getPen()
    pen.moveTo(p1); pen.lineTo(q1); pen.lineTo(q2); pen.lineTo(p2); pen.closePath()
    band.simplify(fix_winding=True)
    return band


def clean_draw(path, pen, tol=6.0, min_area=400.0):
    """Draw a boolean-op result without its micro-artefacts: segments whose
    points all lie within `tol` units of the current point (tiny notches where
    the bowl meets the slash/tail) become plain corners, and slivers smaller
    than `min_area` square units are dropped."""
    rec = RecordingPen(); path.draw(rec)
    contours, cur = [], None
    for op_, args in rec.value:
        if op_ == "moveTo":
            cur = [("moveTo", args)]
        elif op_ in ("closePath", "endPath"):
            contours.append(cur); cur = None
        else:
            cur.append((op_, args))
    for c in contours:
        start = c[0][1][0]; pt = start; kept = [c[0]]
        for op_, args in c[1:]:
            if all(math.hypot(x - pt[0], y - pt[1]) < tol for x, y in args):
                continue
            kept.append((op_, args)); pt = args[-1]
        if len(kept) > 1 and math.hypot(pt[0] - start[0], pt[1] - start[1]) < tol and kept[-1][0] == "lineTo":
            kept.pop()                          # closing point duplicates the start
        poly = [start] + [a[-1] for _, a in kept[1:]]
        area = 0.5 * abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                             for i in range(len(poly))))
        if len(kept) < 3 or area < min_area:
            continue
        for op_, args in kept:
            getattr(pen, op_)(*args)
        pen.closePath()


def rebuild_bowl(font, O0font, n):
    G = path_of(font, n)
    dx = best_dx(G, O0font)
    # parts of the glyph that are not the bowl: subtract a slightly grown
    # old O (drops sub-6u slivers where the glyph's bowl differs from O by
    # rounding), then grow back inside the glyph so the parts still reach
    # the bowl.
    if n == "Oslash":
        # the slash = the strip between its two straight edges, cut by the
        # glyph's own top and bottom (Roboto's slash ends are horizontal).
        # Unioned with the new O this gives clean straight-meets-curve
        # corners, and the slash still runs unbroken through the squarer
        # counter.
        x0, y0, x1, y1 = G.bounds
        box = pathops.Path(); pen = box.getPen()
        pen.moveTo((x0 - 50, y0)); pen.lineTo((x0 - 50, y1)); pen.lineTo((x1 + 50, y1)); pen.lineTo((x1 + 50, y0)); pen.closePath()
        add = op(slash_band(font, n), box, pathops.PathOp.INTERSECTION)
        pieces = [1]
    else:
        # Q's tail: the parts of the glyph that are not the old bowl (minus a
        # 6u margin that drops rounding slivers), grown back 12u inside the
        # glyph so the tail still reaches into the bowl.
        extra = op(G, dilate(path_of(O0font, "O", dx), 6), pathops.PathOp.DIFFERENCE)
        add = op(G, dilate(extra, 12), pathops.PathOp.INTERSECTION)
        pieces = list(add.contours)
    newO = path_of(font, "O", dx)
    res = op(newO, add, pathops.PathOp.UNION)
    gs = font.getGlyphSet()
    tp = TTGlyphPen(gs)
    clean_draw(res, ReverseContourPen(tp))     # TrueType: outer contour clockwise
    g = tp.glyph()
    font["glyf"][n] = g
    g.recalcBounds(font["glyf"])
    return dx, len(pieces)


def main():
    roboto, src, dst = map(Path, sys.argv[1:4])
    dst.mkdir(parents=True, exist_ok=True)
    for s in STYLES:
        f = TTFont(src / f"Sky-{s}.ttf"); R = TTFont(roboto / f"Roboto-{s}.ttf")
        t = TENSION[s]["O"]
        O0 = TTFont(src / f"Sky-{s}.ttf"); RB.rebuild(O0, R, "O", None, 0.0)   # the pre-tension O
        msg = []
        for n in DIRECT:
            tension_direct(f, n, t)
        for n in BOWL:
            dx, k = rebuild_bowl(f, O0, n)
            msg.append(f"{n} dx={dx} parts={k}")
        for n in DIRECT + BOWL:
            adv, _ = f["hmtx"][n]; f["hmtx"][n] = (adv, f["glyf"][n].xMin)
        f.save(dst / f"Sky-{s}.ttf")
        print(f"{s:13s} t={t}  " + "  ".join(msg))


if __name__ == "__main__":
    main()
