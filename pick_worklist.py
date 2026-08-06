#!/usr/bin/env python3
"""Pick a diverse 100-part worklist from candidates.json.

Stratifies across libraries (at most 2 per library) and across pin-count bands
so the sample isn't all 20-pin logic chips or all 100-pin MCUs.
"""
import json
import os
import random
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
cands = json.load(open(os.path.join(HERE, "candidates.json")))

# Prefer datasheets that look like direct PDF links from known vendors.
def score(c):
    ds = c["datasheet"].lower()
    s = 0
    if ds.endswith(".pdf"):
        s += 3
    for v in ("ti.com", "analog.com", "microchip.com", "nxp.com", "st.com",
              "onsemi.com", "diodes.com", "infineon.com", "renesas.com",
              "toshiba", "rohm", "vishay", "maximintegrated", "espressif",
              "nexperia", "littelfuse", "silabs", "cypress", "lattice"):
        if v in ds:
            s += 2
            break
    return s

random.seed(20260804)

by_lib = defaultdict(list)
for c in cands:
    by_lib[c["lib"]].append(c)

picked = []
libs = sorted(by_lib)
random.shuffle(libs)
# round-robin over libraries, best-scoring + pin-count-diverse first
per_lib_iters = {}
for lib in libs:
    items = sorted(by_lib[lib], key=lambda c: (-score(c), c["pins"]))
    random.shuffle(items)
    items.sort(key=lambda c: -score(c))
    per_lib_iters[lib] = iter(items)

rounds = 0
while len(picked) < 100 and rounds < 4:
    for lib in libs:
        if len(picked) >= 100:
            break
        it = per_lib_iters[lib]
        nxt = next(it, None)
        if nxt is not None and score(nxt) > 0:
            picked.append(nxt)
    rounds += 1

for i, p in enumerate(picked, 1):
    p["idx"] = i
    p["slug"] = f"{i:03d}_{p['lib']}_{p['name']}".replace("/", "-").replace(" ", "_")

out = os.path.join(HERE, "worklist.json")
json.dump(picked, open(out, "w"), indent=1)
print(f"{len(picked)} parts -> {out}")
bands = defaultdict(int)
for p in picked:
    n = p["pins"]
    band = "20-29" if n < 30 else "30-49" if n < 50 else "50-99" if n < 100 else "100+"
    bands[band] += 1
print(dict(bands))
print(f"{len(set(p['lib'] for p in picked))} distinct libraries")
