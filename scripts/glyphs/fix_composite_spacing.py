#!/usr/bin/env python3
"""v0.4: accented letters spaced exactly like their base letters.

PROBLEM (measured on v0.3/v0.5 branch): the v0.3 spacing pass re-spaced
base letters (e.g. Regular E: advance 1024 -> 989, outline moved 18u left)
but composite glyphs were only condensed (x 0.88 of Roboto). So E-acute
kept advance 1024, i.e. 35u wider than E, and its accent sat 18u right of
the centre of the E it is attached to. 1,395 of 1,421 composites in Regular
disagreed with their base.

FIX, per composite whose first component is a letter and whose other
components are marks (accents, cedilla, ogonek, dots, strokes):
  advance = base advance + 0.88 * (Roboto composite advance - Roboto base
            advance)   -> usually + 0, so E-acute == E exactly; letters
            Roboto deliberately widens (d-caron, l-caron, Greek tonos)
            keep that extra, condensed.
  base component stays at Roboto's offset * 0.88 (normally 0), so the
            composite inherits the base's side bearings exactly.
  each mark component moves by (base shift - mark shift), where shift =
            how far the v0.3 spacing pass moved that glyph's outline away
            from Roboto * 0.88. The mark therefore sits on the base exactly
            where Roboto put it.
Composites that are not letter+marks (ligatures, digraphs, fractions,
punctuation built from dots) and those with no Roboto counterpart are left
alone and listed in the report.

Usage: python3 fix_composite_spacing.py ROBOTO_DIR IN_DIR OUT_DIR [--report r.json]
"""
import argparse, json, unicodedata
from pathlib import Path
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

STYLES = ["Thin", "Light", "Regular", "Medium", "Bold", "Black",
          "Italic", "MediumItalic", "BoldItalic"]
LETTER = {"Lu", "Ll", "Lt", "Lo", "Lm"}
NOT_MARK = {"Lu", "Ll", "Lt", "Lo", "Nd", "No", "Po", "Pd", "Ps", "Pe", "Sm", "Sc"}  # Lm = spacing accents (circumflex, caron)


def bounds(font, n):
    gs = font.getGlyphSet(); bp = BoundsPen(gs); gs[n].draw(bp); return bp.bounds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roboto"); ap.add_argument("indir"); ap.add_argument("outdir")
    ap.add_argument("--report")
    a = ap.parse_args()
    Path(a.outdir).mkdir(parents=True, exist_ok=True)
    report = {}
    for s in STYLES:
        S = TTFont(Path(a.indir) / f"Sky-{s}.ttf"); R = TTFont(Path(a.roboto) / f"Roboto-{s}.ttf")
        glyf, hmtx, rh = S["glyf"], S["hmtx"], R["hmtx"]
        scmap = {}
        for cp, n in sorted(S.getBestCmap().items()):
            scmap.setdefault(n, cp)
        rcmap = R.getBestCmap()

        def rname(n):
            if n in rh.metrics:
                return n
            alt = n.replace(".c2sc", ".smcp")
            if alt in rh.metrics:
                return alt
            if n in scmap and scmap[n] in rcmap:
                return rcmap[scmap[n]]
            return None

        def cat(n):
            b = n.split(".")[0]
            cp = scmap.get(n, scmap.get(b))
            return unicodedata.category(chr(cp)) if cp is not None else None

        shift_cache = {}

        def shift(n, rn):
            """How far the v0.3 spacing moved Sky glyph n vs Roboto glyph rn * 0.88 (x centre)."""
            if (n, rn) not in shift_cache:
                sb = bounds(S, n)
                rb = bounds(R, rn) if rn in rh.metrics else None
                same = sb and rb and (
                    abs((sb[2] - sb[0]) - 0.88 * (rb[2] - rb[0])) <= 0.06 * 0.88 * (rb[2] - rb[0]) + 12
                    and abs((sb[3] - sb[1]) - (rb[3] - rb[1])) <= 0.15 * (rb[3] - rb[1]) + 12)
                if not same:          # missing, or not the same drawing
                    shift_cache[(n, rn)] = None
                else:
                    shift_cache[(n, rn)] = (sb[0] + sb[2]) / 2 - 0.88 * (rb[0] + rb[2]) / 2
            return shift_cache[(n, rn)]

        rep = {"changed": {}, "skipped": {}}
        for n in S.getGlyphOrder():
            g = glyf[n]
            if not g.isComposite():
                continue
            comps = g.components
            base = comps[0].glyphName
            why = None
            if cat(n) is not None and cat(n) not in LETTER:
                why = f"not a letter ({cat(n)})"
            elif cat(base) not in LETTER and not (cat(base) is None and base.split(".")[0][:1].isalpha() and rname(base)):
                why = f"base {base} is not a letter"
            elif any(cat(c.glyphName) in NOT_MARK for c in comps[1:]):
                why = "ligature/digraph (second component is a letter or symbol)"
            rn = rname(n)
            if not why and rn is None:
                why = "no Roboto counterpart to measure against"
            if not why and not R["glyf"][rn].isComposite():
                why = "Roboto glyph is not a composite"
            if why:
                rep["skipped"][n] = why
                continue
            rcomps = R["glyf"][rn].components
            if len(rcomps) != len(comps):
                rep["skipped"][n] = "component structure differs from Roboto"
                continue
            if abs(hmtx[n][0] - round(0.88 * rh[rn][0])) > 1:
                rep["skipped"][n] = "advance already differs from Roboto*0.88 (hand-adjusted?)"
                continue
            sb = shift(base, rcomps[0].glyphName)
            new_x = []
            ok = True
            for c, rc in zip(comps[1:], rcomps[1:]):
                sm = shift(c.glyphName, rc.glyphName)
                if sm is None or sb is None:
                    ok = False; break
                new_x.append(round(0.88 * rc.x + sb - sm))
            if not ok:
                rep["skipped"][n] = "a component can't be matched to Roboto (missing or a different glyph)"
                continue
            old_adv = hmtx[n][0]
            extra = round(0.88 * (rh[rn][0] - rh[rcomps[0].glyphName][0]))
            adv = hmtx[base][0] + extra
            old_x = [c.x for c in comps]
            comps[0].x = round(0.88 * rcomps[0].x)
            for c, x in zip(comps[1:], new_x):
                c.x = x
            g.recalcBounds(glyf)
            hmtx[n] = (adv, g.xMin)
            rep["changed"][n] = {"base": base, "adv": [old_adv, adv], "base_adv": hmtx[base][0],
                                 "dx": [c.x - o for c, o in zip(comps, old_x)]}
        S.save(Path(a.outdir) / f"Sky-{s}.ttf")
        report[s] = rep
        ch = rep["changed"]
        eq = sum(1 for v in ch.values() if v["adv"][1] == v["base_adv"])
        print(f"{s:13s} composites changed {len(ch)} (advance == base: {eq}); skipped {len(rep['skipped'])}")
    if a.report:
        json.dump(report, open(a.report, "w"), indent=1)


if __name__ == "__main__":
    main()
