#!/usr/bin/env python3
"""Refetch the datasheets whose vendor URL is dead or unreachable, via the Wayback Machine.

Many vendor hosts (st.com, analog.com, datasheets.maximintegrated.com) accept the
TLS handshake from this network and then stall, and several nxp/microchip links are
now 404s or HTML landing pages. The Internet Archive has usable captures of most.
"""
import concurrent.futures as cf
import random
import time
import json
import os
import subprocess
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(os.path.join(HERE, "worklist.json")))
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def curl(url, out=None, timeout=180):
    cmd = ["curl", "-sL", "--max-time", str(timeout), "--retry", "3",
           "--retry-delay", "5", "--retry-all-errors", "-A", UA]
    cmd += ["-o", out] if out else ["-o", "-"]
    cmd.append(url)
    return subprocess.run(cmd, capture_output=not out, text=not out)


def snapshots(url):
    q = urllib.parse.quote(url.split("://", 1)[-1], safe="/:?=&%")
    r = curl(f"http://web.archive.org/cdx/search/cdx?url={q}"
             f"&output=json&fl=timestamp,statuscode,length&filter=statuscode:200&limit=8")
    try:
        rows = json.loads(r.stdout)[1:]
    except Exception:
        return []
    rows.sort(key=lambda x: -int(x[2] or 0))
    return [x[0] for x in rows]


def good(pdf):
    if not os.path.exists(pdf) or os.path.getsize(pdf) < 20000:
        return 0
    with open(pdf, "rb") as f:
        if not f.read(5).startswith(b"%PDF"):
            return 0
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split()[1])
    return 0


def rescue(p):
    time.sleep(random.uniform(0, 3))
    pdf = os.path.join(HERE, "ds", p["slug"] + ".pdf")
    n = good(pdf)
    if n:
        return (p["idx"], "cached", n)
    for ts in snapshots(p["datasheet"])[:4]:
        for _ in range(2):
            curl(f"https://web.archive.org/web/{ts}id_/{p['datasheet']}", pdf)
            n = good(pdf)
            if n:
                return (p["idx"], f"wayback:{ts}", n)
    if os.path.exists(pdf):
        os.remove(pdf)
    return (p["idx"], "FAIL", 0)


with cf.ThreadPoolExecutor(2) as ex:
    for idx, st, n in sorted(ex.map(rescue, W)):
        print(f"{idx:>3} {st:<22} {n}pg", flush=True)
