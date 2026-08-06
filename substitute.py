#!/usr/bin/env python3
"""Replace worklist entries whose datasheet won't download with ones that will.

Vendor hosts st.com / analog.com / datasheets.maximintegrated.com stall from this
network and a number of nxp/microchip/onsemi links are dead, so those parts are
dropped. Replacements are drawn from the same 6445-symbol candidate pool, keeping
one part per library and matching the pin-count band of the part being dropped.
"""
import concurrent.futures as cf
import json
import os
import random
import subprocess
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

W = json.load(open(os.path.join(HERE, "worklist.json")))
CAND = json.load(open(os.path.join(HERE, "candidates.json")))

def band(n):
    return "20-29" if n < 30 else "30-49" if n < 50 else "50-99" if n < 100 else "100+"

have = {int(l.split()[0]) for l in open(os.path.join(HERE, "rescue.log"))
        if "cached" in l}
need = [p for p in W if p["idx"] not in have]
used_libs = {p["lib"] for p in W if p["idx"] in have}
used_names = {(p["lib"], p["name"]) for p in W}
print(f"{len(have)} keepers, {len(need)} to replace", flush=True)

# Hosts already proven unreachable or bot-walled -- don't waste time on them.
BAD_HOST = ("st.com", "analog.com", "maximintegrated", "dialog-semiconductor",
            "invensense", "cypress", "u-blox", "usriot", "parallax", "puyasemi",
            "latticesemi", "xilinx", "renesas.com", "codemercs", "10gtek",
            "mouser.com", "jameco", "chipdb", "cosmacelf", "silabs.com",
            "onsemi.com", "nxp.com", "raspberrypi")

pool = defaultdict(list)
for c in CAND:
    if (c["lib"], c["name"]) in used_names:
        continue
    ds = c["datasheet"].lower()
    if any(h in ds for h in BAD_HOST) or not ds.endswith(".pdf"):
        continue
    pool[c["lib"]].append(c)

random.seed(4242)
for lib in pool:
    random.shuffle(pool[lib])

def try_dl(c):
    tmp = os.path.join(HERE, "ds", "_try_%d.pdf" % (hash((c["lib"], c["name"])) & 0xffffff))
    subprocess.run(["curl", "-sL", "--max-time", "90", "-A", UA, "-o", tmp,
                    c["datasheet"]], capture_output=True)
    ok = False
    if os.path.exists(tmp) and os.path.getsize(tmp) > 20000:
        with open(tmp, "rb") as f:
            ok = f.read(5).startswith(b"%PDF")
    if ok:
        out = subprocess.run(["pdfinfo", tmp], capture_output=True, text=True).stdout
        ok = "Pages:" in out
    if ok:
        return (c, tmp)
    if os.path.exists(tmp):
        os.remove(tmp)
    return (c, None)

# Candidate order: prefer unused libraries, then matching pin band.
wanted_bands = [band(p["pins"]) for p in need]
tried, found = set(), []
libs = sorted(pool)
random.shuffle(libs)
fresh = [l for l in libs if l not in used_libs] + [l for l in libs if l in used_libs]

queue = []
for rnd in range(6):
    for lib in fresh:
        if rnd < len(pool[lib]):
            queue.append(pool[lib][rnd])

with cf.ThreadPoolExecutor(8) as ex:
    for c, tmp in ex.map(try_dl, queue[:900]):
        if tmp:
            found.append((c, tmp))
            print(f"OK   {c['lib']:<26} {c['name']:<26} {c['pins']:>4}p", flush=True)
            if len(found) >= len(need) + 15:
                break

json.dump([{k: v for k, v in c.items()} | {"_tmp": t} for c, t in found],
          open(os.path.join(HERE, "replacements_raw.json"), "w"), indent=1)
print(f"\n{len(found)} downloadable replacements found for {len(need)} slots")
