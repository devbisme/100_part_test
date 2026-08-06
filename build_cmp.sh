#!/bin/bash
# build_cmp.sh <slug>  -- verify+build the generated JPD and diff it against the reference
set -e
cd "$(dirname "$0")"
S="$1"
python /home/devb/projects/skills/datasheet-to-symbol-lib/scripts/verify_jpd.py "gen/$S.jpd"
jpd2spd -o - "gen/$S.jpd" | spd2csv | kipart -w -o "gen/$S.kicad_sym"
echo "===== REFERENCE (KiCad library) ====="
kilib2spd "ref/$S.kicad_sym" -o - 2>/dev/null
echo
echo "===== CMPPARTS ====="
python "$(dirname "$0")/cmp_wrap.py" -g -i properties "ref/$S.kicad_sym" "gen/$S.kicad_sym" || true
echo
echo "===== CMPPARTS (-i units, pin-level) ====="
python "$(dirname "$0")/cmp_wrap.py" -g -i properties -i units "ref/$S.kicad_sym" "gen/$S.kicad_sym" || true
