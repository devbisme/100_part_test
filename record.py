#!/usr/bin/env python3
"""Append one part's verdict to results.jsonl.

    python record.py '<json blob>'

Schema of the blob:
{
  "idx": 1, "slug": "...", "lib": "...", "name": "...", "pins": 28,
  "datasheet": "url",
  "status": "done" | "skipped",
  "skip_reason": "...",              # when skipped
  "cmp_diff_count": 12,              # raw cmpparts difference count (-g)
  "gen_errors":  [ {"kind": "...", "detail": "...", "pins": ["12"]} ],
  "kicad_errors":[ {"kind": "...", "detail": "...", "pins": ["12"]} ],
  "notes": "..."
}
Error `kind` must be one of KINDS below.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results.jsonl")

KINDS = {
    "missing_pin",         # pin in the datasheet absent from the symbol
    "extra_pin",           # pin in the symbol not in the datasheet
    "wrong_pin_number",    # right function, wrong number
    "wrong_pin_name",      # right number, name disagrees with datasheet
    "wrong_pin_type",      # electrical type wrong (input/output/power/passive...)
    "wrong_pin_style",     # graphic style (inverted, clock) wrong
    "missing_alternate",   # datasheet alt function not represented
    "extra_alternate",     # alt function that isn't in the datasheet
    "wrong_unit_split",    # units grouped differently than the datasheet implies
    "wrong_side",          # pin placed on a side that contradicts the pinout diagram
    "wrong_part_scope",    # package/variant modelled wrong (e.g. wrong pin count)
    "property_error",      # datasheet/description/footprint property wrong
    "naming_convention",   # cosmetic name difference only, both defensible
    "hidden_pin",         # pin hidden that shouldn't be
    "other",
}


def main():
    blob = json.loads(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read())
    for side in ("gen_errors", "kicad_errors"):
        for e in blob.get(side, []):
            if e.get("kind") not in KINDS:
                sys.exit(f"bad kind {e.get('kind')!r}; allowed: {sorted(KINDS)}")
    # de-dupe: drop any prior record for the same idx
    rows = []
    if os.path.exists(OUT):
        rows = [json.loads(l) for l in open(OUT) if l.strip()]
    rows = [r for r in rows if r.get("idx") != blob.get("idx")]
    rows.append(blob)
    rows.sort(key=lambda r: r.get("idx", 0))
    with open(OUT, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(f"recorded idx={blob.get('idx')} ({len(rows)} total)")


if __name__ == "__main__":
    main()
