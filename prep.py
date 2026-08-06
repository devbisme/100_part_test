#!/usr/bin/env python3
"""Prepare one worklist entry: pull the reference symbol out, fetch the datasheet.

    python prep.py <idx>

Prints the paths and a pin-count summary of the reference symbol. It does NOT
print the reference pinout -- generation must be done from the datasheet alone.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = json.load(open(os.path.join(HERE, "worklist.json")))

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")


def main():
    idx = int(sys.argv[1])
    p = next(x for x in WORK if x["idx"] == idx)
    slug = p["slug"]
    for d in ("ref", "ds", "gen", "cmp"):
        os.makedirs(os.path.join(HERE, d), exist_ok=True)

    ref = os.path.join(HERE, "ref", slug + ".kicad_sym")
    if not os.path.exists(ref):
        subprocess.run([sys.executable, os.path.join(HERE, "extract_symbol.py"),
                        p["file"], p["name"], ref], check=True)

    pdf = os.path.join(HERE, "ds", slug + ".pdf")
    if not os.path.exists(pdf) or os.path.getsize(pdf) < 5000:
        r = subprocess.run(["curl", "-sL", "--max-time", "120", "-A", UA,
                            "-o", pdf, p["datasheet"]])
        ok = os.path.exists(pdf) and os.path.getsize(pdf) > 5000
        if ok:
            with open(pdf, "rb") as f:
                ok = f.read(5).startswith(b"%PDF")
        if not ok:
            print(json.dumps({**p, "ref": ref, "pdf": None,
                              "download": "FAILED"}, indent=1))
            return

    size = os.path.getsize(pdf)
    pages = ""
    try:
        out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        for line in out.splitlines():
            if line.startswith("Pages:"):
                pages = line.split()[1]
    except FileNotFoundError:
        pass
    print(json.dumps({
        "idx": idx, "slug": slug, "lib": p["lib"], "name": p["name"],
        "pins": p["pins"], "units": p["units"], "datasheet": p["datasheet"],
        "description": p.get("description", ""),
        "ref": ref, "pdf": pdf, "pdf_bytes": size, "pdf_pages": pages,
        "gen_jpd": os.path.join(HERE, "gen", slug + ".jpd"),
        "gen_sym": os.path.join(HERE, "gen", slug + ".kicad_sym"),
    }, indent=1))


if __name__ == "__main__":
    main()
