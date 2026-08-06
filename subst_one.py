import json, os, random, subprocess, sys
HERE=os.path.dirname(os.path.abspath(__file__))
UA=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
W=json.load(open(f"{HERE}/worklist.json"))
CAND=json.load(open(f"{HERE}/candidates.json"))
used_libs={p["lib"] for p in W}
used_names={(p["lib"],p["name"]) for p in W}
BAD=("st.com","analog.com","maximintegrated","renesas.com")
lo,hi=int(sys.argv[1]),int(sys.argv[2])
pool=[c for c in CAND if lo<=c["pins"]<=hi and c["lib"] not in used_libs
      and (c["lib"],c["name"]) not in used_names and c.get("datasheet","").startswith("http")
      and not any(b in c["datasheet"] for b in BAD)]
random.seed(int(sys.argv[3]) if len(sys.argv)>3 else 7)
random.shuffle(pool)
for c in pool[:40]:
    out=f"/tmp/cand.pdf"
    r=subprocess.run(["curl","-sSL","--max-time","70","-A",UA,"-o",out,"-w","%{http_code}",c["datasheet"]],
                     capture_output=True,text=True)
    ok = r.stdout.strip()=="200" and open(out,'rb').read(5)==b"%PDF-"
    print(("OK  " if ok else "bad "), c["lib"], c["name"], c["pins"], c["datasheet"], flush=True)
    if ok:
        print("PICKED"); break
