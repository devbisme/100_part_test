#!/usr/bin/env python3
"""Index every KiCad library symbol with >=20 pins and a datasheet URL."""
import json
import os
import sys
import glob

from simp_sexp import Sexp
from kipart.part import symbol_lib_to_parts

SYMDIR = "/usr/share/kicad/symbols"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "candidates.json")


def pin_count(part):
    n = 0
    for unit in part.get("units", []):
        for side in ("left", "right", "top", "bottom"):
            n += sum(len(p.get("numbers", [])) for p in unit.get(side, []))
    return n


def main():
    rows = []
    for path in sorted(glob.glob(os.path.join(SYMDIR, "*.kicad_sym"))):
        lib = os.path.splitext(os.path.basename(path))[0]
        try:
            with open(path) as f:
                sexp = Sexp(f.read())
            parts = symbol_lib_to_parts(sexp, geometry=False)
        except Exception as e:  # noqa: BLE001
            print(f"skip {lib}: {e}", file=sys.stderr)
            continue
        # find which symbols are derived (extends) -- skip them
        raw = open(path).read()
        for part in parts:
            n = pin_count(part)
            if n < 20:
                continue
            props = part.get("properties", {}) or {}
            ds = props.get("Datasheet") or props.get("datasheet") or ""
            if not ds or not ds.startswith("http"):
                continue
            rows.append({
                "lib": lib,
                "name": part.get("name"),
                "pins": n,
                "units": len(part.get("units", [])),
                "datasheet": ds,
                "description": props.get("Description", ""),
                "keywords": props.get("ki_keywords", ""),
                "file": path,
            })
    with open(OUT, "w") as f:
        json.dump(rows, f, indent=1)
    print(f"{len(rows)} candidates -> {OUT}")


if __name__ == "__main__":
    main()
