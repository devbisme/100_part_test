# 100-Part Symbol Generation Test — Results Summary

**Date:** 2026-08-05
**Skill under test:** `datasheet-to-symbol-lib`
**Reference:** the stock KiCad symbol libraries at `/usr/share/kicad/symbols`

These are the results of testing the Claude skill
[datasheet-to-symbol-lib](https://github.com/devbisme/datasheet-to-symbol-lib)
on 100 parts chosen from the official KiCad symbol libraries.

## What was done

For each of 100 parts:

1. A symbol with ≥20 pins was extracted from a KiCad library (`ref/`).
2. The part's datasheet was downloaded (`ds/`).
3. A symbol was generated **from the datasheet alone** via the skill's pipeline
   — hand-authored JPD → `jpd2spd | spd2csv | kipart` → `.kicad_sym` (`gen/`).
4. The two were diffed with `cmpparts`, then every difference was adjudicated
   by hand against the datasheet and attributed to one side, the other, or
   neither.

Attribution rules are in `CRITERIA.md`. Per-part verdicts are in `results.jsonl`.

**Sample:** 100 parts, 4,986 pins, 77 different KiCad libraries.
Pin counts 20–400, median 29. Two parts were substituted mid-run because no
usable datasheet exists (see *Datasheet availability* below).

## Headline numbers

| | Generated from datasheet | KiCad library |
|---|---:|---:|
| Symbols with zero findings | **67 / 100** | **16 / 100** |
| Pin error rate | **2.77 %** | **21.92 %** |
| Total findings | 138 | 1,093 |
| Parts with ≥1 netlist-affecting error | **14 / 100** | **57 / 100** |

Nine parts were clean on *both* sides.

## Findings by kind

| Error kind | Generated | (parts) | KiCad library | (parts) |
|---|---:|---:|---:|---:|
| missing_alternate | 38 | 6 | **653** | 37 |
| naming_convention | 51 | 15 | 278 | 34 |
| wrong_pin_type | 15 | 3 | **96** | 35 |
| wrong_pin_style | 23 | 7 | 30 | 24 |
| extra_pin | 0 | 0 | 16 | 2 |
| wrong_pin_name | 1 | 1 | 11 | 9 |
| missing_pin | 6 | 3 | 6 | 2 |
| wrong_pin_number | 4 | 2 | 0 | 0 |
| property_error | 0 | 0 | 3 | 3 |
| **TOTAL** | **138** | **33** | **1,093** | **84** |

Two of these categories deserve to be read separately from the rest:

- **`missing_alternate`** measures completeness of optional metadata, not
  netlist correctness. It is 60 % of the KiCad total and is concentrated in
  MCUs where the library symbol names a port pin `PA18` and stops, while the
  datasheet documents six peripheral functions on it. Excluding it, the KiCad
  total drops to 440.
- **`naming_convention`** covers cosmetic-only or equally defensible
  differences and was tallied separately by design; it is not a hard error on
  either side.

Excluding both, the substantive comparison is **generated 49 findings across
14 parts** vs **KiCad 165 findings across 57 parts**.

## Where the KiCad errors are

`wrong_pin_type` (96) is the substantive finding, and it is dominated by whole
symbols typed `passive` throughout rather than by scattered mistakes:

| magnitude | part | kind | issue |
|---:|---|---|---|
| 97 | TMS470R1B768 | wrong_pin_type | nearly every digital I/O typed `passive`; `RST` typed input though the datasheet calls it bidirectional open-drain |
| 16 | 8080 | wrong_pin_type | the 16 address pins typed `output`; HOLD forces the bus to high-Z, so they are tri-state |
| 8 | TPL9201_TSSOP | wrong_pin_type | OUT1–OUT8 typed `output`; they are open-drain low-side sinks |
| 8 | MC3487N / MC3487DX | extra_pin | VCC/GND replicated in all four driver units and the enables in two each — 8 duplicate pins per symbol |
| 8 | KM28C65A, 28C256 | wrong_pin_type | data pins typed `tri_state`; the datasheet and KLC both call for `bidirectional` |
| 7 | MSP430FR5738IRGE | wrong_pin_type | seven port pins typed `input` although the signal-description table gives them as I/O |
| 4 | MSP430F123IRHB | missing_pin | four NC pins absent — 28 pins modelled for a 32-pad QFN |

Two spelling errors also surfaced in the TMS470R1B768 symbol: pin 32 named
`PORST` (should be `PORRST`) and pin 75 named `TDO5` (a stray footnote digit
baked into the pin name).

Error density grows with pin count. In the 33–64 pin band, 20 of 29 generated
symbols were clean and **0 of 29** library symbols were.

| pins | n | generated clean | KiCad clean |
|---|---:|---:|---:|
| 20–32 | 55 | 34 | 13 |
| 33–64 | 29 | 20 | 0 |
| 65–144 | 13 | 11 | 2 |
| 145–400 | 3 | 2 | 1 |

## Where the generated errors are

The generated symbols' failures cluster in two recurring, diagnosable modes.

**1. Active-low bars that `pdftotext` silently deletes.** Overbars live in the
PDF as drawing primitives, not text, so extracted tables lose them entirely.
This produced most of the 23 `wrong_pin_style` findings:

- TMS470R1B768 — 10 pins (`SPIxENA` / `SPIxSCS`), recovered only by rendering
  the package figure at 400 dpi and reading it as an image
- PAL16R8 — 8 registered outputs O1–O8
- Single pins on TPD6S300A, MIC2178, EA_eDIP240J-7LA, CDP1802BCE, ADS8688

**2. Functions documented in prose rather than in the pinout figure.** When a
pin diagram labels a ball `PA08` and the crystal-oscillator role is stated only
in a later section, the generated symbol tends to miss it — the 38
`missing_alternate` findings, e.g. XIN/XOUT/SWCLK/SWDIO on ATSAMD09D14A,
JTAG_TDO/TDI on CC1312R1, VREFA on AVR64DA28, and all 28 peripheral alternates
on the Raspberry Pi 4 header.

The four `wrong_pin_number` findings are the only ones with no systematic
cause: two adjacent-row transpositions (`INC+`/`INC-` on LMH7324, `V+`/`V-` on
DL1416) — plain misreads of a two-column pinout.

`extra_pin` and `property_error` never occurred on the generated side.

## Datasheet availability

Two parts were replaced mid-run because no usable datasheet is obtainable:

- **MCU_Renesas_Synergy_S1 / R7FS12878xA01CFL** — the Synergy S128 datasheet
  has been withdrawn from renesas.com and the URL in the KiCad symbol 404s.
  Replaced with u-blox ZED-F9P.
- **FPGA_Lattice / LFXP2-5E-5TN144** — the LatticeXP2 datasheet contains no
  per-pin table at all, and Lattice's separate Pin & Package files are
  login-gated (HTTP 403). Replaced with Microchip DSPIC33EP256MU810-xPT.

One part was recovered rather than dropped: the Efinix **T8Q144xx** datasheet
has no pin numbers, but the vendor's companion *Trion Packaging User Guide*
(Figure 17) does. Checking for a packaging document before discarding a part is
worth doing.

## Tool bugs found

1. **`kipart/compare_parts.py:127`** — `_normalize()` calls `name.lower()` on an
   `int`, crashing on purely numeric part names (e.g. `8080`). Fix: `str(name)`.
2. **`kilib2spd`** — two fidelity issues: lossy pin-name-sequence compression
   (seen on Omega2S+) and a phantom De Morgan unit (seen on ATSAME70J21A).
3. **`verify_jpd.py:82`** — the `FOOTNOTE_TAIL` check false-positives on
   bus-index pin names ending in a single-digit bracket (`HET[0]`, `ADIN[3]`),
   reporting *"still carries a footnote marker"*. This blocked the TMS470R1B768
   build; the verifier had to be bypassed for that part.

## Caveats

- **The 100 are not 100 independent trials.** Conventions settled while
  adjudicating early parts (recorded in `CRITERIA.md`) informed how later parts
  were generated. The generated-side numbers are therefore optimistic relative
  to a cold start.
- **Single adjudicator.** The same agent generated the symbols and judged both
  sides. Judgement calls that could have gone either way — supply-typing
  disagreements, `passive` on analog nodes, clock style on dual-purpose GPIOs —
  were waived on both sides for consistency, but they were still one person's
  calls.
- **`cmpparts` produced the raw diff; it did not produce the verdicts.** Every
  difference was resolved by reading the datasheet.
- The sample skews toward MCUs and interface ICs because those dominate the
  KiCad libraries at ≥20 pins; connectors and passives are under-represented.

## Files

| path | contents |
|---|---|
| `results.jsonl` | 100 per-part verdicts, one JSON object each |
| `CRITERIA.md` | error-attribution rules (what counts, what is an accepted convention) |
| `STATE.md` | run log and method |
| `ds/` | the 100 datasheets |
| `ref/` | the KiCad library symbols, extracted individually (157 files — derived `extends` symbols and the originals of the two substituted parts are included) |
| `gen/` | the 100 generated JPDs and their built `.kicad_sym` files |
| `build_cmp.sh` | verify + build one JPD and diff it against its reference |
| `tabulate.py` | regenerates the tables above from `results.jsonl` |

`cmp/` is present but empty — `cmpparts` output was read inline during the run
rather than archived. Re-run `build_cmp.sh <slug>` to reproduce any single diff.
