#!/usr/bin/env python3
"""Reproduce the v0.5 repaired fonts from the v0.3 release, in order.

  v0.3 TTFs (git 060051b:fonts/)
    1. scripts/glyphs/repair_v02_zone.py  undo the v0.2 x-height scaling in
                                          caps, figures and cap-height symbols
    2. scripts/glyphs/rebuild_O_o.py      rebuild O/o from Roboto with the
                                          approved tension (o_tension.json)
    3. scripts/fix_metrics.py             lsb = xMin for every glyph; italic
                                          angle + caret = measured slant
  -> fonts/Sky-*.ttf   (then run scripts/make-webfonts.py for the website)

Step 1 inverts a scaling, so it must start from the v0.3 outlines, not from
already-repaired fonts; this script always starts from the v0.3 commit.

Usage: python3 scripts/build-v05-repair.py /path/to/roboto-unhinted [--out fonts]
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
        run(py, ROOT / "scripts/glyphs/rebuild_O_o.py", a.roboto_dir, "--in", td / "s1",
            "--out", td / "s2", "--tension-json", ROOT / "scripts/glyphs/o_tension.json")
        run(py, ROOT / "scripts/fix_metrics.py", td / "s2", a.out)


if __name__ == "__main__":
    main()
