#!/usr/bin/env python3
"""Extract one symbol from a KiCad library into its own .kicad_sym file.

    python extract_symbol.py <lib.kicad_sym> <SymbolName> <out.kicad_sym>
"""
import sys

from simp_sexp import Sexp


def main():
    libfile, name, out = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(libfile) as f:
        lib = Sexp(f.read())

    header = [lib[0]]
    keep = None
    for item in lib[1:]:
        if isinstance(item, list) and item and item[0] == "symbol":
            if str(item[1]).strip('"') == name:
                keep = item
        elif isinstance(item, list):
            header.append(item)
    if keep is None:
        sys.exit(f"symbol {name!r} not found in {libfile}")
    if "extends" in str(keep):
        # derived symbol: caller should have filtered these out
        print(f"warning: {name} extends another symbol", file=sys.stderr)
    new = Sexp(header + [keep])
    with open(out, "w") as f:
        f.write(str(new))
    print(out)


if __name__ == "__main__":
    main()
