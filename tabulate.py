#!/usr/bin/env python3
"""Tabulate the recorded errors across all processed parts."""
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(os.path.join(HERE, "results.jsonl")) if l.strip()]
done = [r for r in rows if r.get("status") == "done"]
skipped = [r for r in rows if r.get("status") != "done"]

gen = Counter()
kic = Counter()
gen_parts = Counter()
kic_parts = Counter()
for r in done:
    gk = set()
    kk = set()
    for e in r.get("gen_errors", []):
        gen[e["kind"]] += max(1, len(e.get("pins", [])))
        gk.add(e["kind"])
    for e in r.get("kicad_errors", []):
        kic[e["kind"]] += max(1, len(e.get("pins", [])))
        kk.add(e["kind"])
    for k in gk:
        gen_parts[k] += 1
    for k in kk:
        kic_parts[k] += 1

total_pins = sum(r.get("pins", 0) for r in done)
gen_total = sum(gen.values())
kic_total = sum(kic.values())

print(f"Parts processed: {len(done)}   skipped: {len(skipped)}   pins compared: {total_pins}")
print()
w = 22
print(f"{'error kind':<{w}} {'generated':>10} {'gen parts':>10} {'kicad lib':>10} {'kic parts':>10}")
print("-" * (w + 44))
for k in sorted(set(gen) | set(kic), key=lambda k: -(gen[k] + kic[k])):
    print(f"{k:<{w}} {gen[k]:>10} {gen_parts[k]:>10} {kic[k]:>10} {kic_parts[k]:>10}")
print("-" * (w + 44))
print(f"{'TOTAL':<{w}} {gen_total:>10} {len([r for r in done if r.get('gen_errors')]):>10} "
      f"{kic_total:>10} {len([r for r in done if r.get('kicad_errors')]):>10}")
print()
if done:
    print(f"Generated symbols perfect:      {sum(1 for r in done if not r.get('gen_errors'))}/{len(done)}")
    print(f"KiCad library symbols perfect:  {sum(1 for r in done if not r.get('kicad_errors'))}/{len(done)}")
    print(f"Generated pin error rate:       {gen_total/total_pins*100:.2f}% of pins" if total_pins else "")
    print(f"KiCad pin error rate:           {kic_total/total_pins*100:.2f}% of pins" if total_pins else "")
print()
if skipped:
    print("Skipped:")
    for r in skipped:
        print(f"  {r['idx']:>3} {r['lib']}:{r['name']} - {r.get('skip_reason','')}")
