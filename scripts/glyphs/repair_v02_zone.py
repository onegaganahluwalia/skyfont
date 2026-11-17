#!/usr/bin/env python3
"""v0.5 family repair — undo the v0.2 x-height scaling where it never belonged.

WHAT WENT WRONG (measured, see docs/design/README.md §3b):
  v0.2 lowered the x-height by scaling every point with 0 < y <= ~1104 by
  k = 990/1102 ~= 0.898 (italics ~0.896) — in EVERY glyph, not only the
  lowercase. Points above ~1104 and below the baseline were left alone.
  Capitals, figures and cap-height symbols therefore had their lower ~75%
  squashed: crossbars lowered and thinned (H bar 157u -> 141u), bottom
  strokes ~10% light, bowls (B P R) shrunk, italic stems kinked at y~1104.
  x was never touched by that step (verified: x residuals ~0).

METHOD:
  Target = Roboto v2.138 per-weight outline + Sky's documented transforms
  (x: v0.3 condensing/spacing as already in the file; y: unscaled for
  cap-height designs). Because the squash touched y only, the exact way to
  reach that target while keeping everything Sky added on top (corner
  softening, spacing, advance widths, kerning) is to invert it on the Sky
  outline: y = y_sky / k for 0 < y_sky <= k*1100 (and, in the band up to
  k*1112, wherever that reading matches Roboto better — the italic zone top
  was ~1106-1110), then snap each point to
  the Roboto y of the same glyph when within 2.5u (removes rounding), and
  carry that snap to chamfer partners so corner-softening stays 9u.

SCOPE (detected per glyph, per style, by measurement against Roboto):
  restore: squashed glyphs that are not x-height designs — uppercase (all
  scripts, incl. ss06 alternates), lining figures, Nl, currency, and
  punctuation / symbols / modifier & superscript letters whose Roboto
  design reaches cap height (yMax >= 1300).
  keep: lowercase and their small-cap/unicase/oldstyle forms, numr/dnom
  (standardised in v0.2), combining marks, punctuation/symbols below cap
  height (x-height relative), titlecase digraphs (mixed), O/o (rebuilt by
  rebuild_O_o.py).

Usage: python3 repair_v02_zone.py ROBOTO_DIR IN_DIR OUT_DIR [--report r.json]
"""
import argparse, json, statistics, sys, unicodedata
import numpy as np
from fontTools.pens.basePen import BasePen
from collections import defaultdict
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

STYLES = ["Thin", "Light", "Regular", "Medium", "Bold", "Black",
          "Italic", "MediumItalic", "BoldItalic"]
ZONE_TOP = 1104
ZONE_LO, ZONE_HI = 1100, 1112   # ambiguous band at the zone top
LOWER_SUF = {"c2sc", "unic", "smcp", "oldstyle", "numr", "dnom", "sinf", "subs", "sups"}


def coords(font, n):
    g = font["glyf"][n]
    c, e, f = g.getCoordinates(font["glyf"])
    return list(c), list(e), list(f)


def fit_k(S, R):
    rs = []
    for n in S.getGlyphOrder():
        if n not in R["glyf"].glyphs:
            continue
        a, b = S["glyf"][n], R["glyf"][n]
        if a.numberOfContours <= 0 or b.numberOfContours <= 0:
            continue
        ca, _, _ = coords(S, n); cb, _, _ = coords(R, n)
        if len(ca) != len(cb):
            continue
        for (_, ys), (_, yr) in zip(ca, cb):
            if 200 < yr <= ZONE_TOP and abs(ys / yr - 0.898) < 0.02:
                rs.append(ys / yr)
    return statistics.median(rs)


def status(S, R, n, k):
    ys = [y for _, y in coords(S, n)[0]]
    yr = [y for _, y in coords(R, n)[0]]
    zs = [y for y in ys if 4 < y <= k * ZONE_TOP]
    if not zs:
        return "nozone"
    yrz = [y for y in yr if 0 < y <= ZONE_TOP + 6]
    sq = it = 0
    for y in zs:
        m1 = any(abs(y - k * r) <= 2.5 for r in yrz)
        m2 = any(abs(y - r) <= 2.5 for r in yr)
        sq += m1 and not m2
        it += m2 and not m1
    if sq >= max(2, 0.5 * len(zs)):
        return "squashed"
    if it >= 0.5 * len(zs):
        return "intact"
    return "mixed"


def category(S, n, rev, inv):
    if rev.get(n):
        return unicodedata.category(chr(min(rev[n])))
    b = n.split(".")[0]
    return unicodedata.category(chr(inv[b])) if b in inv else "?"


def decide(S, R, n, st, rev, inv):
    if st not in ("squashed", "mixed"):
        return "keep", st
    if n in ("O", "o"):
        return "keep", "O/o rebuilt separately"
    c = category(S, n, rev, inv)
    suf = set(n.split(".")[1:])
    gr = R["glyf"][n]; gr.recalcBounds(R["glyf"])
    if suf & LOWER_SUF:
        return "keep", f"{c} x-height/fraction form"
    if c == "Lu":
        return "restore", "uppercase"
    if c == "Lt":
        return "keep", "titlecase digraph"
    if c == "Nd":
        return "restore", "lining figure"
    if c in ("Nl", "Sc"):
        return "restore", c
    if c in ("Mn", "Me"):
        return "keep", "combining mark"
    if c == "Ll":
        return "keep", "lowercase"
    if (c in ("Lm", "Lo", "No") or c[0] in "PS") and gr.yMax >= 1300:
        return "restore", f"{c} cap-height form"
    return "keep", f"{c} below cap height"


def unsquash(S, R, n, k):
    c, ends, flags = coords(S, n)
    ry = sorted({y for _, y in coords(R, n)[0]})
    raw, snapd = [], {}
    def near(v):
        return min((abs(r - v) for r in ry), default=1e9)
    for i, (x, y) in enumerate(c):
        inv = 0 < y <= k * ZONE_LO
        if k * ZONE_LO < y <= k * ZONE_HI:
            # boundary band: the v0.2 zone top was 1104 in uprights but up
            # to ~1110 in italics; decide by which reading matches Roboto
            inv = near(y / k) <= near(y) + 2
        if inv:
            yy = y / k
            best = min(ry, key=lambda r: abs(r - yy)) if ry else None
            if best is not None and abs(best - yy) <= 2.5:
                snapd[i] = best - yy
            raw.append(yy)
        else:
            raw.append(None)
    # carry snaps to unsnapped neighbours (corner-softening chamfers)
    start = 0
    out = []
    contour_of = {}
    for ci, e in enumerate(ends):
        for i in range(start, e + 1):
            contour_of[i] = (start, e)
        start = e + 1
    for i, (x, y) in enumerate(c):
        if raw[i] is None:
            out.append((x, y)); continue
        d = snapd.get(i)
        if d is None:
            s, e = contour_of[i]
            nb = [s + ((i - s + j) % (e - s + 1)) for j in (-1, 1)]
            cand = [snapd[j] for j in nb if j in snapd and raw[j] is not None and abs(raw[j] - raw[i]) < 20]
            d = cand[0] if cand else 0.0
        out.append((x, round(raw[i] + d)))
    # corner-softening: an orthogonal corner is a 2-point chamfer, 8u in x
    # (9u * 0.88 condensing; 6-10u in italics, slanted) and 9u in y.
    # Re-apply that exact 9u wherever the inverse mapping touched an
    # unsnapped chamfer point.
    for i in range(len(c)):
        if raw[i] is None or i in snapd:
            continue
        s, e = contour_of[i]
        for j in (s + ((i - s - 1) % (e - s + 1)), s + ((i - s + 1) % (e - s + 1))):
            dx = abs(c[j][0] - c[i][0]); dy0 = c[i][1] - c[j][1]
            if 5 <= dx <= 11 and 6 <= abs(dy0) <= 10 and (j in snapd or raw[j] is None):
                out[i] = (out[i][0], out[j][1] + (9 if dy0 > 0 else -9))
                break
    g = S["glyf"][n]
    g.coordinates = GlyphCoordinates(out)
    g.recalcBounds(S["glyf"])


class _Flatten(BasePen):
    """Flatten an outline to polygons (handles implied on-curves)."""
    def __init__(self, gs, steps=6):
        super().__init__(gs); self.steps = steps; self.polys = []; self.cur = None
    def _moveTo(self, p): self.cur = [p]; self.polys.append(self.cur)
    def _lineTo(self, p): self.cur.append(p)
    def _qCurveToOne(self, a, b):
        p0 = self.cur[-1]
        for i in range(1, self.steps + 1):
            t = i / self.steps; m = 1 - t
            self.cur.append((m*m*p0[0] + 2*m*t*a[0] + t*t*b[0], m*m*p0[1] + 2*m*t*a[1] + t*t*b[1]))
    def _curveToOne(self, a, b, c):
        p0 = self.cur[-1]
        for i in range(1, self.steps + 1):
            t = i / self.steps; m = 1 - t
            self.cur.append(tuple(m**3*p0[j] + 3*m*m*t*a[j] + 3*m*t*t*b[j] + t**3*c[j] for j in (0, 1)))
    def _closePath(self): pass
    def _endPath(self): pass


def _polys(font, n):
    gs = font.getGlyphSet(); pen = _Flatten(gs); gs[n].draw(pen)
    return [p for p in pen.polys if len(p) > 1]


def shape_distance(S, R, n):
    """Mean distance (font units) from the Sky outline to the Roboto outline,
    Roboto x-fitted to Sky's x extent (Sky's x is condensed/spaced) and y as
    designed. Structure-independent, so it also works for glyphs Sky has
    redrawn with different point structures; corner-softening contributes
    a small constant (~0.1u)."""
    P = _polys(S, n); Q = _polys(R, n)
    if not P or not Q:
        return 0.0
    sx = [x for p in P for x, _ in p]; rx = [x for q in Q for x, _ in q]
    a = (max(sx) - min(sx)) / ((max(rx) - min(rx)) or 1); b = min(sx) - a * min(rx)
    pts = np.array([pt for p in P for pt in p], float)
    A = np.array([(a * q[i][0] + b, q[i][1]) for q in Q for i in range(len(q))], float)
    B = np.array([(a * q[(i + 1) % len(q)][0] + b, q[(i + 1) % len(q)][1]) for q in Q for i in range(len(q))], float)
    AB = B - A; L = (AB ** 2).sum(1); L[L == 0] = 1e-9
    AP = pts[:, None, :] - A[None]
    t = np.clip((AP * AB[None]).sum(2) / L[None], 0, 1)
    d = np.sqrt(((pts[:, None, :] - (A[None] + t[..., None] * AB[None])) ** 2).sum(2)).min(1)
    return float(d.mean())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roboto"); ap.add_argument("indir"); ap.add_argument("outdir")
    ap.add_argument("--report")
    a = ap.parse_args()
    report = {}
    Path(a.outdir).mkdir(parents=True, exist_ok=True)
    for s in STYLES:
        S = TTFont(Path(a.indir) / f"Sky-{s}.ttf"); R = TTFont(Path(a.roboto) / f"Roboto-{s}.ttf")
        k = fit_k(S, R)
        rev = defaultdict(list); inv = {}
        for cp, n in sorted(S.getBestCmap().items()):
            rev[n].append(cp); inv.setdefault(n, cp)
        rep = {"k": k, "glyphs": {}}
        for n in S.getGlyphOrder():
            if n not in R["glyf"].glyphs:
                continue
            g = S["glyf"][n]
            if g.numberOfContours <= 0 or R["glyf"][n].numberOfContours <= 0:
                continue
            st = status(S, R, n, k)
            d, why = decide(S, R, n, st, rev, inv)
            entry = {"status": st, "decision": d, "why": why}
            if d == "restore":
                before = shape_distance(S, R, n)
                saved = GlyphCoordinates(g.coordinates)
                unsquash(S, R, n, k)
                after = shape_distance(S, R, n)
                if after > before + 0.3:          # never make a glyph worse
                    g.coordinates = saved; g.recalcBounds(S["glyf"])
                    entry.update(decision="reverted", why=why + " (repair did not improve fit)")
                entry.update(dist_before=round(before, 2), dist_after=round(after, 2))
            rep["glyphs"][n] = entry
        S.save(Path(a.outdir) / f"Sky-{s}.ttf")
        report[s] = rep
        nres = sum(1 for v in rep["glyphs"].values() if v["decision"] == "restore")
        nrev = sum(1 for v in rep["glyphs"].values() if v["decision"] == "reverted")
        print(f"{s:13s} k={k:.4f} restored {nres} reverted {nrev}")
    if a.report:
        json.dump(report, open(a.report, "w"), indent=1)


if __name__ == "__main__":
    main()
