#!/usr/bin/env python3
"""check_names.py <slug>: every pin name and alternate in gen_sonnet/<slug>.jpd must appear in the datasheet text.
Catches typos/hallucinated names, not misplacement. Skips PDFs with no text layer."""
import json, re, subprocess, sys, glob
slug = sys.argv[1]
pdf = glob.glob(f"ds/{slug}.pdf")[0]
txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
norm = lambda s: re.sub(r'[^a-z0-9+\-]', '', s.lower())
hay = norm(txt)
if len(hay) < 2000: print("no text layer; skipped"); sys.exit(0)
jpd = json.load(open(f"gen_sonnet/{slug}.jpd"))
missing = set()
for part in jpd["parts"]:
    for u in part["units"]:
        for side in ("left", "right", "top", "bottom"):
            for p in u.get(side, []):
                if "name" not in p: continue
                for n in [p["name"]] + [a["name"] for a in p.get("alternates", [])]:
                    k = norm(n)
                    if k and k not in hay: missing.add(n)
print("not found in datasheet text:", sorted(missing) if missing else "none")
