# Verdicts (generated vs ref, judged against the datasheet). G=generated wrong, R=ref wrong, -=none
002 74LS241: numbers all match; names differ (ref generic I0/O0). G:- R:-
004 TPD6S300A: R: D1/D2 typed passive. G:-
010 ATSAMD09D14A: numbers match. G:- R:- (ref folds XIN/XOUT/SWCLK/SWDIO/RST into names; mine are alternates; alternates verified vs table)
012 USB2504: numbers match. R: CFG_SEL0 typed input (IOSD12 I/O). RBIAS typed input vs I-R (debatable). G:-
023 LMH7324: numbers match. Judgement: DAP passive (mine) vs power_in (ref). G:- R:-
033 ESP32-C3: numbers match. R: CHIP_EN typed bidirectional (datasheet I); XTAL_N/P typed bidirectional (datasheet "-"). G:-
036 DL1416: match. G:- R:-
053 MCP23S17: R: SCK no clock style; INTA/INTB tri_state (datasheet O). G:-
064 AVR64DA28: R: PF6 typed bidirectional (input-only), UPDI typed input (bidirectional). G:- (alternates verified vs table)
072 PAL16R8: R: CLK no clock style. G:- (O1-O8 inverted per logic diagram; ref agrees)
005 TPA3251: numbers match. R: visible power pins 11,14,20,23,24,43,44 typed passive; OSC_IOP typed bidirectional (datasheet O). G:-
008 ADS8688: numbers match. R: none substantive (analog nodes passive, accepted). G:- (cosmetic: RST/PD bar)
013 TPS70348: numbers match; ref adds pad pin 25 (datasheet gives no number; KiCad convention). R:- G:-
016 DAC5578: numbers match; ref adds pad pin 25 (datasheet gives no number). R:- G:-
017 74LS244: numbers match; ref uses positional names. R:- G:-
004 (revised): thermal pad omitted (unnumbered in datasheet); ref has pad as pin 21 (KiCad convention) and types D1/D2/GND-pins passive. R: D1/D2 passive.
018 MC3487N: numbers/types match once units merged; ref repeats VCC/GND/ENABLE per unit (KiCad merges same-number pins; netlist-neutral). R:- G:-
019 CD4097B: numbers match (pinout only in the logic-diagram figure; no pin table for 4097). R:- G:-
021 SN75160B: numbers match. R: PE typed active-low (no overbar in datasheet figure). G:-
056 MC3487DX: same datasheet and result as 018. R:- G:-
061 GD75232DW: numbers match. R:- G:-
043 HEF4093B: numbers match; ref names gate pins "~", calls VDD/VSS "VCC"/"GND" (naming). R:- G:-
055 ATF16V8B: numbers match (datasheet gives I/O pins no individual names). R:- G:-
062 ISOW7744: numbers match. R(weak): GND2 typed power_out (datasheet: ground connection). G:-
063 LSF0108: numbers match. R:- G:-
096 TXB0108PW: numbers match. R:- G:-
065 28C256: numbers match. R: 8 data pins typed tri_state (datasheet: data inputs/outputs). G:-
075 KM28C65A: numbers match. R: 8 data pins tri_state (datasheet I/O); RDY/BSY typed output (datasheet: open-drain). G:-
076 27256: numbers match. Judgement: VPP power_in (mine) vs input (ref); names O0-7 vs ref D0-7 (cosmetic). R:- G:-
067 8080A: numbers match. R: phi1/phi2 lack clock style. Judgement: address pins tri_state (mine, HOLD text) vs output (ref, table O). G:-
068 CDP1802BCE: numbers match. R: CLOCK input has no clock style. (XTAL passive vs ref output: judgement) G:-
047 8259A-2: numbers match. R: CAS0/CAS1/CAS2 typed input/output/output (datasheet I/O for all). G:-
032 INA253: numbers match; R: none (analog passive accepted). G:-
050 BQ24610: numbers match; ref adds pad pin 25. R: VFB typed output (feedback input). Judgement: BTST/PH power_in(ref) vs passive. G:-
024 BQ24167RGE: numbers match; ref adds pad pin 25. R: many inputs typed passive (IUSB1-3, ILIM, BOOT, TS, VDPM-class), IN supply typed input; SYS/DRV types differ from table. G:-
030 TLC5971RGE: numbers match (pad is pin 18 per datasheet; ref adds 25). R: SCKI no clock style. Judgement: OUT typed open_collector (ref) vs output. G:-
082 TPS70345: same datasheet/result as 013. R:- G:-
077 TPS26630RGE: numbers match; ref adds pad pin 25. R:- G:-
098 TPS26400RHF: numbers match; ref adds pad pin 25. R(minor): RTN typed passive. G:-
099 OPA569DWP: numbers match; ref adds pad 21 and abbreviates names. Judgement: ISET/Parallel Out typed output (ref) vs passive. R(minor): ISET output. G:-
080 UCC1895J: numbers match; R: none (analog passive accepted). G:-
086 MIC2178: numbers match. R: COMP typed input (datasheet: error-amp output); BIAS typed input (datasheet: internal bias output); PWRGD typed output (datasheet: open-drain). G:-
060 TPD12S520DBT: numbers match. R(minor): all GND/TMDS_GND and TMDS IO pins typed passive. G:-
100 AT42QT1060-M: numbers match; ref adds pad pin 29. R: SDA typed bidirectional / SCL input (datasheet: open drain). G: INITIAL ERROR - I missed the overbar on CHG (caught by viewing figure; fixed, not counted in final file).
090 MCP39F521: numbers match. R: SDA typed bidirectional (datasheet: open drain); OSCI no clock style. Judgement: DR no_connect (mine, 'must be left floating') vs output ~{DR} (ref). G:-
031 LCD-016N002L: numbers match; A1/K1/A2/K2 LED pads are drawn but unnumbered in the datasheet - I used the ref-style names (ASSUMPTION, flagged). R:- G:-
029 eDIP240J-7LA: numbers match. R: SPI/I2C alternates missing on pins 6-15, 20 (9+ missing_alternate). G:- (overbar on SBUF unverified)
057 OLED-128O064D: numbers match. R: serial-mode alternates (SDIN, SCLK, SDA_OUT, SA0, ~{WR}, ~{RD}) missing. G:-
054 SFP: numbers match; ref adds CAGE pad (not in datasheet). R(minor): VeeT/VeeR typed passive. G:-
026 PY32F002AF15P: numbers match. R: ~90 missing_alternate (only SWD/BOOT0/OSC/NRST named). Alternates read from AF mapping image tables 3-3/3-4/3-5 (nearest-row text parsing was WRONG for PA0/PA1 - corrected by image). G:-
034 ATtiny841-M: numbers match after fixing my own pin-order error on 16/19/20 (text extraction of rotated labels reversed; caught by cmpparts, confirmed by image). R: alternates missing (PCINT/ADC/TOCC/..). G: initial error (fixed).
073 MSP430F123IRHB: numbers match incl. 4 NC (ref also has them). R:- G:-
015 MSP430FR5738IRGE: numbers match. R: RST/NMI/SBWTDIO, P2.0-2.2, P1.6, P1.7, PJ.4, PJ.5 typed input (datasheet I/O) - 8 wrong_pin_type; VCORE typed input. G:-
093 ATSAMD21E17A-A: numbers match. R: ~170 alternates missing (ref has none). Alternates extracted mechanically from Table 7-1 by column x-position; PA22-PA25 merged band resolved by hand from tokens (cross-checked with device knowledge). G:- (alternate types are my rule-based assignment)
066 AT90USB162-16A: numbers match. R: nearly all alternates missing; XTAL2 typed bidirectional (output); RESET typed bidirectional. G:- (read directly from pinout figure)
058 ATmega324PV-10M: numbers match; ref adds pad pin 45. R(minor): AREF typed passive, supply dups passive. G:- (read from QFN figure)
020 AT90CAN128-16A: numbers match. R(minor): AREF typed passive; VCC/GND dups passive; ref AGND naming. G:- (read from TQFP figure)
070 AVR64DA48: numbers match; ref adds pad 49 and lacks alternates. R: PF6 typed bidirectional (input-only), UPDI typed input. G:- (alternates extracted mechanically from the PDF mux table by column)
083 PIC16F884-IP: numbers and types match; ref folds alternates into names. R:- G:-
084 PIC18F4455-IP: numbers match. R: VUSB typed bidirectional (3.3V regulator output). G:- (overbars on UOE/OESPP not verifiable from text)
092 PIC18F4450-IML: numbers match. R: VUSB typed bidirectional (regulator output). G:- (read from QFN figure)
048 AT89x51 (TQFP44): numbers match. R: MOSI/MISO alt types swapped; ~{RD} typed input (output); XTAL2 typed input (datasheet: output of oscillator amplifier). G:- (read from figure image)
046 TPL9201: numbers match; ref adds pad 21. R: OUT1-8 typed output (open-drain low-side); RST typed bidirectional vs open drain; Judgement: NCS active-low bubble. G: INITIAL MISS - SCLK clock style (found via cmpparts; fixed).
041 SLA7078MPRT: numbers match. R: Clock input lacks clock style. Judgement: SenseA/B output (ref) vs passive. G:-
035 RPM5.0-6.0: pads match; R:- G:-
037 RPMH24-1.5: pads match; R:- G:-
049 MCP25625-SS: numbers match. R: SCK and OSC1 lack clock style. G:-
052 ENC28J60-ML: numbers match. R: pin1 named ~{WOL} typed output (datasheet: reserved NC); VCAP typed input (regulator output); VSSRX/VSSTX typed power_out; SCK no clock style. G:-
039 HV5622PG: numbers match. G: INITIAL ERRORS - HVOUT typed output (datasheet title: open-drain outputs) and missing overbars on LE/BL/POL (datasheet prints them) - both caught by viewing page 1, fixed. R: CLK no clock style. NOTE: datasheet text says LE transfers when 'high' despite overbar name.
079 MCS3142: numbers match. R: SCK-like PGC no clock style. Judgement: pin7 'No connection; tie to Vss' = NC (mine) vs VSS power_in (ref); analog SOSC/XTAL types. G:-
078 SE5004L: numbers match; ref adds pad 21. R: pin1 named GND/power_in (datasheet: NU, open circuit). G:-
071 SpinWarrior24R6: matches ref exactly. R:- G:-
006 HD44780U: numbers match (80). R: OSC1 no clock style. Judgement: V1-V5 typed input (ref) vs power_in; ref names R/~{W} (datasheet text prints no bar). G:-
011 ATF1504ASVL (TQFP44): numbers match. R: pin 38 named I/OE1/Vpp - datasheet never mentions Vpp (unsupported alt). Names: mine IO_MC<n>, ref I/O (cosmetic). G:- (JTAG/PD/GCLK alts read from Table 1-6/1-7)
014 RN42: numbers match (32; RN42N-only pins excluded); ref adds SHIELD pin 36 (not in datasheet). Judgement: GPIO types. G:-
089 AT86RF233-Z: numbers match; ref adds EPAD 33. R: SCLK no clock style; XTAL1/2, RFP typed passive. Judgement: DVDD/AVDD power_in vs regulator output. G:-
091 BMF055: numbers match. R: PA24 typed input (datasheet: general-purpose IO); function names embedded in pin names. G:- (RESETN kept as printed)
059 SIM900: numbers match. R: SCL typed output (I2C clock, datasheet I/O); GND/VBAT dup pins passive (accepted). Judgement: SDA typed bidirectional (datasheet 'O' looks like a typo). G:-
081 Raspberry_Pi_4: numbers match. R: ~166 alternates missing (ref carries only a few: SDA_I2C1, SPI0, UART, PWM...). G:- (alternates parsed mechanically from Table 5; types by name rule)
095 LAN9514: numbers match; ref adds pad 65. R: TEST1/TEST4 typed input (datasheet: leave unconnected); TEST2/3 input; EXRES typed input; RXP typed input (AIO); several VDD dups passive. G:- (n-prefixed names kept w/ active-low style)
097 FE310-G000: numbers match after inference on pins 3/4. G: datasheet figure prints QSPI_DQ_2 twice and no DQ_0 (typo); I initially copied it literally; now DQ_1/DQ_0 INFERRED (not stated in the figure) - flagged. R: AON_*_N bars as ~{} (equivalent); ~40 alternates (PWM/SPI1/UART0) missing; VDD/IVDD dup pins passive. (exposed paddle numbered 49 in datasheet.)
025 CC1312R1F3RGZ: numbers match; ref adds EGP pad 49. R: TCKC no clock style; X32K_Q1/Q2, X48M typed input (crystal pins); judgement: DCOUPL power_out(ref) vs passive; RF_P/N typed passive. G:-
027 ZED-F9P: numbers match; ref adds pad 55. R: some VCC/GND dup pins passive; SPI_SDO/SDI named SPI_MISO/MOSI (cosmetic). G:-
074 C8051F384-GQ: numbers match. R: RST/C2CK typed input (datasheet: D I/O open-drain). G:-
069 PIC24FJ64GA306: numbers match (top row text order reversed - fixed from image). R: alternates folded into names; ref types all alternates bidirectional; VCAP typed passive. G:-
028 PIC24FJ256DA210: numbers match (100). R: pin 39 named RF31 (datasheet label RP31/.../RF13; RF31 does not exist); VUSB (pin 55) typed bidirectional (supply); alternates folded into names for some. G:- (top/bottom rows from rotated-char helper + image; wrapped right-side labels corrected by eye)
007 dsPIC33FJ64MC710A: numbers match (100); ref encodes alternates inside pin names (pin-name info equals mine). G:- R:- (read from page-12 figure; overbars SS1/SS2/FLTA/FLTB/U*RTS/CTS/MCLR verified in image)
038 PIC32MX795F512L: numbers match (100); alternates parsed mechanically from Table 9 text; ref carries far fewer alternates (226 only in mine). R: see name diffs (some alternates folded into names; VUSB3V3/VBUS naming). G:-
040 ATSAME70J21A-AN: numbers match (64). R: ~177 alternates missing; VDDIO/GND/VDDCORE dup pins passive. G:- (table extracted by x-columns from Table 6-3; NRST input_low style dropped by kipart because the pin is bidirectional)
003 ATSAME70Q19A-AN + 044 ATSAMV71Q21B-A: same datasheet (DS60001527D); numbers match (144 each); alternates (397 each) extracted from Table 6-1 by x-columns; supply rows (VDDIO/VDDCORE/GND stacks) added from the comma-list rows. R: VREFN typed bidirectional (datasheet I); 044: VDDOUT typed power_in (regulator output); 397 alternates missing. G:- (3 polluted rows fixed by hand: 85 TST, 137 HSDP, 143 VDDPLLUSB)
094 ATSAML21G16B-MUT: numbers match (48); ref adds pad 49; R: VDDCORE typed power_in (regulated output); ~252 alternates missing. G:- (pinout from figure image; Table 7-1 G column via pdftotext -bbox; PB10/PB11/PA30/PA31 rows added from layout text)
042 Omega2S+: numbers match (63 in datasheet); ref adds pin 64 GND (not in datasheet). R: HW_RST_N lacks active-low style; GND/WIFI_RF typed passive. Judgement: WLED_N output. G:-
045 MT41K256M16TW: 96 balls match; ref uses subscripted names; supply dups passive (accepted); A10/AP and A12/BC# alternates modelled by me, folded into names in ref. R:- G:-
051 MSP432E401Y: numbers match (128). G: INITIAL MISS - overbars on WAKE (64) and HIB (65) (found via ref diff, confirmed in figure; fixed). R: VREFA+ typed power_in vs analog input (judgement); supply dups passive; ~288 alternates missing. (pin table parsed from Table 4-2 text; types from table)
088 TMS470R1B768: numbers match (144). R: 132 of 144 pins typed passive (I/O, inputs, supplies, NC); pin 32 named PORST (datasheet PORRST); pin 75 named TDO5 (datasheet TDO); GIOA[n]/INTn alternates omitted; ref lacks SPI*ENA/SCS bars except pin 1 inverted. G:- (verify_jpd false-positive 'footnote marker' on bus-index names like HET[0] bypassed; kipart build succeeded; SPI3 overbar assumed, not seen in figure)
087 ATSAMA5D21 (TFBGA196): 196 balls match; table 6-2 196-pin column parsed by regex, stacked supply rows (VDDIODDR/VDDCORE/GND*/VDDIOP*) resolved from bbox x-column; 128 PIO rows with A-G peripheral alternates. R: ADVREF, VBG, DDR_VREF typed power_in/passive (datasheet I; judgement); N3 named ~{RST} vs datasheet NRST; DDR_RESETN renamed ~{DDR_RESET} (naming convention); supply stack dups passive-hidden (accepted); ~380 alternates missing. G:- (verify_jpd warnings about numbered-name stacks ignored)
085 dsPIC33EP256MU810 (TQFP-100; replaces Lattice LFXP2): numbers match (100); names from pin diagram p.9 (top/bottom rotated labels via bbox + image), types from Table 1-1. R: MCLR lacks bar (printed overbar confirmed in image); VUSB3V3 typed bidirectional (datasheet P); VBUS bidirectional (datasheet I); ref folds all alternate functions into slash-names (e.g. 'RC15/CLKO/OSC2') instead of alternates (convention); stacked VSS dups passive-hidden (accepted). G:- (main name = port pin RXn, alternates = other functions: my convention; alt types rule-based from Table 1-1; VCAP typed power_in per datasheet 'P')
022 Efinix T8Q144xx: NOT BUILT. ds/022 (T8 data sheet) has pin-function tables and signal names but no ball/pin numbers anywhere (README: numbers come from separate Trion Packaging User Guide, not in ds/ and not to be downloaded); rule 'never invent pin numbers' => no symbol; ref (144 pins) not assessable from ds/.
009 CCGM1A1 (FBGA-324): 324 balls match; parsed Table 5.3 (pin list by ball, 1st/2nd function rows -> primary/alternate). R: config pins (JTAG_*, CFG_MD*, POR_EN, CFG_DONE/FAILED_N) typed bidirectional vs datasheet-direction (my input/output; datasheet group says GPIO, direction is my inference from function); POR_ADJ passive vs my input; RST_N renamed ~{RESET}, N.C. renamed NC, alternates folded into slash-names (convention); supply dups passive-hidden (accepted). G: direction of config pins is inference (table gives group only).
001 Samtec ASP-134486-01: 400 positions A1..K40 (rows A-K no I, 40 columns, 400 solder charges per BOM) from mechanical drawing only; numbers match ref (400); no pin names/functions in datasheet -> I named pins by position, all passive; ref names Pin_n (naming only). Ref also holds sibling ASP-134602-01 (not in ds). G: row-letter set read from image; position=letter+column is a convention inference (drawing gives no per-pin table).
