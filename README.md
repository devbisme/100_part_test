# 100-Part Symbol Generation Test — Sonnet Run vs. KiCad Library

**Date:** 2026-10-30
**Branch:** `sonnet`
**Generator:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), medium effort
**Skill under test:** `datasheet-to-symbol-lib` v3.0.0
**Reference:** the stock KiCad symbol library parts, extracted to `ref/`

This README reports a second pass over the same 100 parts. Every symbol was
rebuilt from its datasheet in `ds/` (nothing re-downloaded) and compared with
the KiCad library symbol in `ref/`. An earlier run (a different model, results
in `gen/` and `results.jsonl`) was **not consulted** while building these.

## What was done

For each part:

1. The datasheet in `ds/` was read (text extraction plus rendered page images
   for pinout figures, overbars and rotated labels).
2. A JPD was authored and verified, then built with
   `jpd2spd | spd2csv | kipart` into `gen_sonnet/<slug>.kicad_sym`.
3. The result was diffed against `ref/<slug>.kicad_sym` with `cmpparts`
   (`-m pins`, geometry/properties/units ignored; see `cmp_wrap.py`).
4. Each difference was adjudicated against the datasheet and recorded in one
   line in `gen_sonnet/verdicts.md` as a **G** (generated side wrong) or **R**
   (reference side wrong) finding, or as neither.

Rules for what counts as an error versus an accepted convention are in
`CRITERIA.md`.

## Headline results

| | |
|---|---|
| Symbols built | **99 / 100** |
| Not built | 022 Efinix T8Q144xx — the datasheet has no pin numbers (see below) |
| Pin numbers agreeing with the KiCad symbol | **essentially all** on the 99 built parts; the reference's extra unnumbered pad/shield pins are the only unmatched pins I recorded (below) |
| Parts with a generated-side error left in the final file | **none known** — see "Generated-side errors" for what was caught and the items that remain judgement or inference |
| Parts with ≥1 reference-side finding (any severity) | **≈72 of 98** assessed |
| Parts with no reference-side finding recorded | ≈26 |

The reference-side tally is counted from the one-line verdicts, not from a
per-pin finding log as in the earlier run, and includes minor items (e.g. an
analog node typed `passive`). Treat it as approximate. No per-error-kind
totals are given because they were not tabulated.

## What was wrong in the KiCad library symbols

Judged against the datasheet. Ordered roughly by how often they occurred.

1. **Pin types.** Whole symbols typed `passive` for digital I/O, inputs and
   supplies, e.g. TMS470R1B768 (132 of 144 pins `passive`). Other cases:
   supplies typed `passive` or `bidirectional` (VUSB3V3 on dsPIC33EP256MU810; also
   VUSB, VCAP and VFB on other parts), `input` pins typed `bidirectional` (CHIP_EN on
   ESP32-C3, VBUS on dsPIC33EP256MU810), data pins on the 28C256 / KM28C65A
   EEPROMs typed `tri_state` where the datasheet says I/O, and open-drain
   outputs typed `output` (TPL9201 OUT1–8).
2. **Missing active-low or clock styling.** Examples: MCLR (dsPIC33EP256MU810,
   overbar confirmed in the figure), SCK on MCP23S17, CLK on PAL16R8 and
   HV5622, HW_RST_N on Omega2S+. Some bars are spurious instead (PE on
   SN75160B has none in the datasheet figure).
3. **Name errors.** TMS470R1B768: pin 32 `PORST` (datasheet `PORRST`) and
   pin 75 `TDO5` (datasheet `TDO`). Also pin 39 `RF31` on PIC24FJ256DA210
   (should be `RF13`), pin 1 `~WOL` on ENC28J60, and SE5004L pin 1 `GND` where
   the datasheet says NU. SAMA5D21 N3 is `~{RST}` against the datasheet's
   `NRST`.
4. **Alternate functions mostly absent.** On MCUs the library names the port
   pin and stops, or folds functions into a slash name (`RC15/CLKO/OSC2`,
   `IO_WA_A8/~{SPI_CS}`). The generated symbols carry them as alternates:
   roughly 90–400 per MCU, e.g. about 380 not present in the SAMA5D21 reference
   and about 250 on the SAML21. This is the largest difference by count, but it
   is metadata completeness, not netlist correctness.
5. **Extra pad/shield pins.** The reference adds pins for thermal pads, shields
   and cages that the datasheets give no number for (RN42, SFP, TPS70348,
   DAC5578, TPS26400, OPA569 and others). I did not invent numbers for
   unnumbered pads, so these show as extra pins in the reference. KiCad
   convention arguably justifies them; they are not counted as errors.
6. **Smaller items.** Duplicated supply pins per unit (MC3487), missing NC
   pins (MSP430F123 modelled with 28 pins for a 32-pad package), unsupported
   names (`Vpp` on ATF1504).

Differences I treated as **conventions, not errors** (consistent with
`CRITERIA.md`): hidden stacked duplicate supply pins typed `passive`, `passive`
on analog nodes, positional or abbreviated names where the datasheet gives none,
pin placement, case, and the reference folding alternates into the name.

## Generated-side errors

Final files: no known pin-number errors. Errors I made and caught during the
run, all fixed before the final build:

| part | error | how found |
|---|---|---|
| 28C256 | I/O pin numbers shifted (GND given a data-pin number) | `verify_jpd` duplicate-number check |
| ATtiny841 | top-row order wrong (rotated labels extracted in reverse) | `cmpparts`, confirmed in image |
| AT42QT1060, MSP432E401Y | missed overbars (CHG; WAKE, HIB) | figure image / ref diff |
| TPL9201 | SCLK missing clock style | ref diff |
| HV5622 | HVOUT typed output (datasheet: open drain); overbars on LE/BL/POL missed | page image |
| TPD6S300A | invented a number for the unnumbered thermal pad | review |
| 003 / 044 | three polluted rows in the Table 6-1 extraction (pins 85, 137, 143) | hand-checked |

Items that remain **judgement or inference**, not verified facts:

- **FE310-G000 pins 3/4.** The datasheet figure prints `QSPI_DQ_2` twice and
  no `DQ_0`. I set pins 3/4 to `DQ_1` / `DQ_0` by inference.
- **GateMate CCGM1A1.** The pin table gives only a signal group; the
  input/output direction of JTAG, CFG_MD, POR_EN and CFG_DONE/FAILED_N is my
  inference from the function.
- **Reference-voltage and decoupling pins** (SAMA5D21 ADVREF, VBG, DDR_VREF;
  dsPIC33EP256MU810 VCAP) are typed from the datasheet type column (`I`, `P`); the reference disagrees
  in places and either reading is defensible.
- **TMS470R1B768 SPI3 overbar** is assumed by analogy with SPI1/2/4/5, not seen
  in the figure.
- **Alternate types** (input/output/bidirectional on alternates) come from a
  rule, not from a per-function reading of the datasheet.
- **Samtec ASP-134486-01 (001).** The datasheet is a mechanical drawing with no
  signal list. I derived 400 positions (rows A–K, no I; columns 1–40) from the
  drawing and named pins by position, all `passive`. That matches the
  reference's numbering; it is a convention, not a datasheet fact.

## Alternates verification

Alternate functions were checked mechanically against the datasheet tables
(extraction by x-column or `pdftotext -bbox`, then a name check with
`gen_sonnet/check_names.py`) for ATSAMD09D14A, ESP32-C3, AVR64DA28 / AVR DA
family, ATSAMA5D21, the SAM E70 / S70 / V70 / V71 family, ATSAML21, and several
others; zero real mismatches were found. Many other parts were generated from
slash-names or Pin-function columns and checked only by the name-presence
script. Composed alternate names (for example AVR `AC0_AINN0`) legitimately do
not appear verbatim in the text.

## Datasheet availability

- **Substituted parts.** Two parts were replaced in the original run because no
  usable datasheet exists: Renesas Synergy S1 R7FS12878xA01CFL
  (datasheet withdrawn) and Lattice LFXP2-5E-5TN144 (no per-pin table; pin files
  login-gated). The replacements (u-blox ZED-F9P and Microchip
  dsPIC33EP256MU810-xPT) were used here; stale files for the substituted parts
  remain in `ref/`, so use exact slugs when globbing.
- **022 Efinix T8Q144xx — not built.** The data sheet lists signal names but no
  ball or pin numbers. The numbers are in the separate *Trion Packaging User
  Guide*, which is not in `ds/`; I did not invent numbers and did not download
  it. The reference's 144 pins could not be assessed.
- **Shared datasheets.** 003 / 040 / 044 are one PDF (SAM E70/S70/V70/V71,
  DS60001527D); 013 / 082 share TPS703xx; 018 / 056 share MC3487; 064 / 070
  share the AVR DA family.

## Caveats

- **Not blind.** I read this README (the earlier version, which listed failure
  modes) before starting. Some fixes were prompted by seeing the reference diff;
  each was confirmed against the datasheet. The earlier run's `gen/` and
  `results.jsonl` were not read.
- **Single adjudicator.** The same agent generated the symbols and judged both
  sides; there is no independent check. Judgement calls are listed above.
- **Pilot first.** Ten parts were done first and the method adjusted; later
  parts benefit from that.
- **Datasheet defects and extraction limits.** Rotated top/bottom labels and
  overbars are lost or scrambled by text extraction; I checked against rendered
  figures where it mattered, but not for every pin of every part.
- **Reference-side counts are approximate** and mix severities (see above).
- The sample skews toward MCUs and interface ICs.

## Tool issues seen

1. **`verify_jpd.py`** — the footnote check false-positives on bus-index names
   such as `HET[0]` and `ADIN[3]` ("still carries a footnote marker"). It also
   flagged `GIOA[7]` on the TMS470. The kipart build succeeds regardless; I
   bypassed the check for TMS470R1B768. The check can also fire on real
   footnote suffixes like `NRST(3)` and `TCK(4)`, which must be stripped.
2. **`cmpparts` pairing.** `ref/` files often hold sibling parts, so
   `cmpparts` pairs the wrong ones; `-a REFNAME=genname` aliasing is needed.
   `cmp_wrap.py` fixes a crash on purely numeric part names (e.g. `8080`).
3. **`kilib2spd`** dumps are lossy; I did not trust them for reference contents.
4. **`kipart`** drops `output_low` on `open_collector` pins and `input_low` on
   `bidirectional` pins, so the bar is placed in the name (`~{NAME}`) for those.

## Files

| path | contents |
|---|---|
| `gen_sonnet/` | **this run:** per-part `.jpd` and built `.kicad_sym` (99 parts) |
| `gen_sonnet/verdicts.md` | one-line adjudication per part (generated vs reference vs datasheet; `G:` generated-side, `R:` reference-side) |
| `gen_sonnet/STATE.md` | run state and method notes |
| `gen_sonnet/check_names.py` | checks every pin/alternate name appears in the datasheet text |
| `ds/` | the 100 datasheets (not re-downloaded) |
| `ref/` | the KiCad library symbols (derived `extends` symbols and originals of substituted parts included) |
| `CRITERIA.md` | error-attribution rules |
| `cmp_wrap.py` | `cmpparts` wrapper used for the diffs |
| `gen/`, `results.jsonl`, `tabulate.py`, `build_cmp.sh` | the **earlier** run (different model); not used or updated here. Its README, with its own headline numbers, is in git history |

To reproduce one diff:

```
python cmp_wrap.py -m pins -t 0.3 -g -i properties -i units \
    [-a REFNAME=genname] ref/<slug>.kicad_sym gen_sonnet/<slug>.kicad_sym
```
