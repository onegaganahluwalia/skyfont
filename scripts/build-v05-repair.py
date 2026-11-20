#!/usr/bin/env python3
"""Reproduce the v0.4 fonts from the v0.3 release, in order.

  v0.3 TTFs (git 060051b:fonts/)
    1. scripts/glyphs/repair_v02_zone.py       undo the v0.2 x-height scaling
                                               in caps, figures, cap-height symbols
    2. scripts/glyphs/fix_composite_spacing.py accented letters spaced exactly
                                               like their base letters
    3. scripts/glyphs/restore_low_punct.py     round dots: . , ; : ‚ „ · • ¡ ¿
    4. scripts/glyphs/rebuild_O_o.py           O/o from Roboto, approved tension
    5. scripts/glyphs/round_caps_tension.py    C G Q D Ø Œ inherit the O curve
    6. scripts/fix_metrics.py                  lsb = xMin; italic angle = measured
    7. scripts/set_release.py                  version fields, xAvgCharWidth
  -> fonts/Sky-*.ttf   (then run scripts/make-webfonts.py for the website)

Step 1 inverts a scaling, so it must start from the v0.3 outlines, not from
already-repaired fonts; this script always starts from the v0.3 commit.

Usage: python3 scripts/build-v05-repair.py /path/to/roboto-unhinted [--out fonts] [--version 0.4.0]
Roboto: https://github.com/googlefonts/roboto/releases/tag/v2.138
"""
import argparse, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V03 = "060051b"
STYLES = ["Thin", "Light", "Regular", "Medium", "Bold", "Black",
          "Italic", "MediumItalic", "BoldItalic"]


def run(*cmd):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roboto_dir")
    ap.add_argument("--out", default=str(ROOT / "fonts"))
    ap.add_argument("--version", default="0.4.0")
    ap.add_argument("--reports", help="copy the per-glyph JSON reports here")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        v03 = td / "v03"; v03.mkdir()
        for s in STYLES:
            data = subprocess.run(["git", "-C", str(ROOT), "show", f"{V03}:fonts/Sky-{s}.ttf"],
                                  check=True, capture_output=True).stdout
            (v03 / f"Sky-{s}.ttf").write_bytes(data)
        py = sys.executable
        run(py, ROOT / "scripts/glyphs/repair_v02_zone.py", a.roboto_dir, v03, td / "s1",
            "--report", td / "repair-report.json")
        run(py, ROOT / "scripts/glyphs/fix_composite_spacing.py", a.roboto_dir, td / "s1", td / "s2",
            "--report", td / "composite-report.json")
        run(py, ROOT / "scripts/glyphs/restore_low_punct.py", a.roboto_dir, td / "s2", td / "s3")
        run(py, ROOT / "scripts/glyphs/rebuild_O_o.py", a.roboto_dir, "--in", td / "s3",
            "--out", td / "s4", "--tension-json", ROOT / "scripts/glyphs/o_tension.json")
        run(py, ROOT / "scripts/glyphs/round_caps_tension.py", a.roboto_dir, td / "s4", td / "s5")
        run(py, ROOT / "scripts/fix_metrics.py", td / "s5", td / "s6")
        run(py, ROOT / "scripts/set_release.py", a.version, td / "s6", a.out)
        if a.reports:
            import shutil
            Path(a.reports).mkdir(parents=True, exist_ok=True)
            for r in ("repair-report.json", "composite-report.json"):
                shutil.copy(td / r, Path(a.reports) / r)

if __name__ == "__main__":
    main()
