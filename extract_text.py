#!/usr/bin/env python3
"""Extract symbols from a .kicad_sym by slicing the original text.

Round-tripping through simp_sexp drops the quoting on string atoms, which
corrupts any value that itself contains a double quote (e.g. a Description of
'.160", 4-Digit ...') and makes the result unparseable. Slicing the source text
keeps every symbol byte-identical to the library.
"""
import json
import os
import re
import sys
from collections import defaultdict


def split_symbols(text):
    """Yield (name, start, end) for each top-level (symbol ...) block."""
    i, n = 0, len(text)
    depth = 0
    in_str = False
    esc = False
    sym_start = None
    while i < n:
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "(":
            if depth == 1 and text[i:i + 8] == "(symbol ":
                sym_start = i
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 1 and sym_start is not None:
                block = text[sym_start:i + 1]
                m = re.match(r'\(symbol\s+("(?:[^"\\]|\\.)*"|\S+)', block)
                name = m.group(1).strip('"') if m else None
                yield name, sym_start, i + 1
                sym_start = None
        i += 1


def parent_of(block):
    m = re.search(r'\(extends\s+("(?:[^"\\]|\\.)*"|\S+)\)', block)
    return m.group(1).strip('"') if m else None


def main():
    W = json.load(open("worklist.json"))
    by_file = defaultdict(list)
    for p in W:
        by_file[p["file"]].append(p)
    bad = []
    for f, ps in by_file.items():
        text = open(f).read()
        blocks = {}
        first = None
        for name, s, e in split_symbols(text):
            blocks[name] = text[s:e]
            if first is None:
                first = s
        header = text[:first].rstrip()
        for p in ps:
            chain, cur = [], p["name"]
            while cur in blocks:
                chain.append(blocks[cur])
                cur = parent_of(blocks[cur])
            if not chain:
                bad.append(p["slug"])
                continue
            body = "\n".join(reversed(chain))
            open(f"ref/{p['slug']}.kicad_sym", "w").write(header + "\n" + body + "\n)\n")
    print(f"{len(W) - len(bad)} refs written; missing: {bad}")


if __name__ == "__main__":
    main()
