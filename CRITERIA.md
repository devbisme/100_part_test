# Error-attribution criteria

An "error" is a deviation from what the datasheet states. Judged the same way
for the generated symbol and the KiCad-library symbol.

## Counted as errors
- wrong_pin_number  - right function, wrong number
- missing_pin / extra_pin - pin present in the datasheet but not the symbol, or vice versa
- wrong_pin_name    - name contradicts the datasheet's name column (not mere formatting)
- wrong_pin_type    - type contradicts the datasheet's function: power pin typed as
                      signal, output typed as input, bidirectional typed as input-only
- wrong_pin_style   - spurious or missing active-low indication; missing clock
                      indication only on pins the datasheet designates as clock
                      *inputs* (clock outputs and crystal pins are left to taste)
- missing_alternate / extra_alternate
- wrong_unit_split, wrong_side (contradicts the pinout diagram), wrong_part_scope
- property_error
- hidden_pin        - a *signal* pin hidden (not the stacking/NC conventions below)

## NOT counted as errors (accepted KiCad library conventions)
- Stacking duplicate same-name pins: one visible power_in + the rest hidden/passive
- Hiding NC / DNC pins
- `passive` for analog signal pins where the datasheet says "Analog in/out"
- Pin placement, side choice, body size, unit numbering
- Case of pin names

## naming_convention
Cosmetic-only or equally defensible differences (e.g. renaming a documented
"NC - connect to ground" pin to GND, adding an index suffix to two identically
named pins). Tallied separately; not a hard error.
