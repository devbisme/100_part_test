# Run state — KiCad symbol generation vs library comparison

**Working dir:** `/tmp/claude-1000/-home-devb-projects-skills-datasheet-to-symbol-lib/1dc09771-30da-4ee1-846d-33dfd76e5096/scratchpad/eval`

## Task
Loop 100×: pick a KiCad library symbol with ≥20 pins, download its datasheet,
generate a symbol from the datasheet with the `datasheet-to-symbol-lib` skill,
compare against the library symbol with `cmpparts`, record errors on both sides.
Tabulate at the end.

## Progress
**100 of 100 recorded.** Run complete; final tabulation produced.

## Files
- `worklist.json` — the 100 parts (idx, lib, name, pins, datasheet URL, slug)
- `results.jsonl` — one record per finished part (schema in `record.py`)
- `ds/<slug>.pdf` — datasheet; `ref/<slug>.kicad_sym` — library symbol;
  `gen/<slug>.jpd` + `.kicad_sym` — generated symbol
- `CRITERIA.md` — what counts as an error vs an accepted KiCad convention
- `tabulate.py` — prints the running tally; `record.py` — appends a result
- `build_cmp.sh <slug>` — verify + build the JPD, dump the ref, run cmpparts twice
  (once normally, once with `-i units` for pin-level diffs)
- `cmp_wrap.py` — cmpparts with a local fix for numeric part names (kipart bug)
- `extract_text.py` — re-extracts ref symbols by text-slicing (simp_sexp round-trip
  corrupts values containing a `"`)

## Method per part
1. `pdfinfo ds/<slug>.pdf` — confirm the datasheet is actually for this part
2. Find the pinout figure for the **exact package** (suffix decodes it; check the
   ordering table if unsure)
3. **Crop dense/small figures at 400–600 DPI** with `pdftoppm -x -y -W -H` before
   reading — full-page renders caused two transposition errors (DL1416, LMH7324)
4. Check for a **separate alternate-function table** and the figure's **colour
   legend** — both carry functions the pin labels don't
5. Read the **Pin Definitions table** for types; don't infer type from pin name
6. Write `gen/<slug>.jpd`, run `build_cmp.sh <slug>`, attribute each diff, `record.py`

## Remaining 10 parts
38 PIC32MX795F512L 100 · 51 MSP432E401Y 128 ·
3 ATSAME70Q19A-AN 144 · 22 T8Q144xx 144 · 44 ATSAMV71Q21B-A 144 · 85 LFXP2-5E-5TN144 144 ·
88 TMS470R1B768 144 · 87 ATSAMA5D21 196 · 9 CCGM1A1 324 · 1 Samtec_ASP-134486-01 400

## Tally at 90 parts / 3,162 pins
| kind | generated | kicad |
|---|---|---|
| missing_alternate | 38 | 647 |
| wrong_pin_type | 15 | 89 |
| wrong_pin_style | 13 | 25 |
| extra_pin | 0 | 16 |
| missing_pin | 6 | 6 |
| wrong_pin_name | 1 | 9 |
| wrong_pin_number | 4 | 0 |
| property_error | 0 | 3 |
| naming_convention (not an error) | 45 | 258 |

Exact on both sides: 15/90. Generated-clean: 60/90.

## Points to carry into the final write-up
- My only `wrong_pin_number` errors (4, in 2 parts) were both **two adjacent labels
  transposed on a small figure**; KiCad has zero. High-DPI cropping fixed the habit.
- My `missing_alternate`/`missing_pin` errors are almost all **information outside
  the pinout figure** — mechanical drawings, colour legends, separate mux tables
  (LCD-016N002L, SFP, SAMD09, Raspberry_Pi_4, CC1312R).
- KiCad's `missing_alternate` (297) is concentrated in ~20 MCU symbols, three of
  them Microchip AVRs that drop the entire peripheral mux. It measures completeness
  of optional metadata, not netlist correctness — **report the tally with and
  without it**.
- KiCad's `extra_pin` (16) is 2 symbols duplicating VCC/GND across units.
- Two `property_error`s: MIC2178 → mic2177.pdf; PIC18F4455 → PIC18F2450/4450 doc
  (pinouts genuinely differ at 3 pins).
- Recurring accepted-convention calls: stacked hidden power pins, hidden NCs,
  `passive` on analog/RC-node pins, layout and unit choices, name case.
- **Caveat for the write-up:** later parts benefited from lessons surfaced by earlier
  comparisons (e.g. VREFA on the AVR64DA48 after missing it on the DA28), so the
  100 parts are not 100 independent trials.
- Second kipart issue to report: `kilib2spd` over-compresses pins into one SPD
  row with several numbers when the names are NOT an increment sequence (seen on
  Omega2S+: `UART_TXD0/GPIO_12 39 40`, where pin 40 is actually UART_RXD0/GPIO_13),
  and `spd2csv` then drops the extra numbers - a lossy round trip. All comparisons
  in this run were made with cmpparts on the .kicad_sym files, so results stand.
- Renesas Synergy S128 (idx 27) was dropped: the datasheet URL in the KiCad symbol
  now redirects to the S3A6 user manual and the S128 document is gone from
  renesas.com. Replaced with RF_GPS:ZED-F9P (55 pins).
- Method note that earned its keep: always read reference pin names from the raw
  .kicad_sym (or from cmpparts), never from the kilib2spd SPD dump - the dump
  compresses name sequences lossily and renders the De Morgan-common block as a
  phantom extra unit.
- kipart bug to report: `compare_parts.py:127` `_normalize()` calls `name.lower()`
  on what the s-expression reader returns as an `int` for purely numeric part names
  (e.g. `8080`) → crash. Fix: `str(name)`.
