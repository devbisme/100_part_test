# sonnet run state (branch `sonnet`)
Rebuild from ds/*.pdf into gen_sonnet/, compare to ref/ with cmpparts. Did NOT read gen/ or results.jsonl.
Per-part adjudications: gen_sonnet/verdicts.md (one line each). Helper: gen_sonnet/check_names.py <slug>.
Method: pdftotext -> locate pin table; render figure for overbars + rotated top/bottom labels (pdftotext reverses/scrambles
rotated labels: ALWAYS check order against the image); write JPD (python generator using mk.py in the session scratchpad);
verify_jpd.py; jpd2spd|spd2csv|kipart -w; cmp_wrap.py -m pins -t 0.3 -g -i properties -i units [-a REF=gen] ref/<slug>.kicad_sym gen_sonnet/<slug>.kicad_sym.
Thermal/exposed pads with NO number in the datasheet are omitted (skill: never invent a number).
Done 87/100. TODO: 1:001_Connector_Samtec_ASP-134486-01(400), 3:003_MCU_Microchip_SAME_ATSAME70Q19A-AN(144), 9:009_FPGA_CologneChip_GateMate_CCGM1A1(324), 22:022_FPGA_Efinix_Trion_T8Q144xx(144), 40:040_MCU_Microchip_SAME_ATSAME70J21A-AN(64), 42:042_MCU_Module_Omega2S+(64), 44:044_MCU_Microchip_SAMV_ATSAMV71Q21B-A(144), 45:045_Memory_RAM_MT41K256M16TW(96), 51:051_MCU_Texas_MSP432E401Y(128), 85:085_FPGA_Lattice_LFXP2-5E-5TN144(144), 87:087_MCU_Microchip_SAMA_ATSAMA5D21(196), 88:088_MCU_Texas_TMS470R1B768(144), 94:094_MCU_Microchip_SAML_ATSAML21G16B-MUT(49)
Self-caught generated-side errors so far (fixed): 065 data-pin numbers, 100 CHG overbar, 034 pin order from rotated text, 046 SCLK clock style, 039 HVOUT open-drain + LE/BL/POL bars, 097 QSPI_DQ typo (inferred).
STATE: 095/100 done; 088 verdict recorded; TODO 001 009 022 085 087
STATE (final): 99/100 built (jpd+kicad_sym in gen_sonnet/); 022 not built (no pin numbers in ds). All verdicts in verdicts.md. Nothing committed.
