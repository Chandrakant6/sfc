# Satisfactory Factory BOM Calculator

A simple, deterministic Python tool to generate a **Bill of Materials (BOM)** tree for any item in Satisfactory (Update 1.0+).  
It shows exactly which **standard recipes** and **machines** are needed to produce 1 unit of the target item, recursing down to raw resources (ores, oil, water, etc.).

## Features

- Uses only **standard (non-alternate)** recipes — no "Alternate: Turbo Whatever"
- Correctly treats raw resources as mine/extract only (no fake recipes like limestone → iron ore)
- Clean ASCII tree output showing:
  - Recipe name
  - Machine/building
  - Exact ingredient quantities
  - Recursion to sub-components and raw nodes
- Cycle detection (just in case)
- Interactive: enter any item key name (e.g. `rotor`, `plastic`, `supercomputer`)
- Relies on Kirk McDonald's official data (`data.json`)

## Example Output (for `rotor`)

```
Target item (e.g. rotor, plastic, motor, computer) or 'quit': rotor

┌── Required to produce 1 × Rotor
└── rotor  [Rotor – Assembler]
│   └── 25 × screw
│       └── screw  [Screw – Constructor]
│           └── 1 × iron-rod
│               └── iron-rod  [Iron Rod – Constructor]
│                   └── 1 × iron-ingot
│                       └── iron-ingot  [Iron Ingot – Smelter]
│                           └── 1 × iron-ore
│                               └── iron-ore  (RAW RESOURCE – mine / extract)
    └── 5 × iron-rod
        └── iron-rod  [Iron Rod – Constructor]
            └── 1 × iron-ingot
                └── iron-ingot  [Iron Ingot – Smelter]
                    └── 1 × iron-ore
                        └── iron-ore  (RAW RESOURCE – mine / extract)

──────────────────────────────────────────────────────────────────────
```


## Requirements

```
- Python 3.6+
- `data.json` file (official Satisfactory recipe data)
```

## Setup

### 1. Download the latest data file:

https://raw.githubusercontent.com/KirkMcDonald/satisfactory-calculator/master/data/data.json

Right-click → Save As → name it `data.json` in the same folder as the script.

### 2. Save the calculator code as `bom_calc.py`.

### 3. Run:

```
python bom_calc.py
```

### 4. Enter item key names when prompted (examples below).

Common Item Key Names

- Item,Key name
- Rotor,rotor
- Plastic,plastic
- Modular Frame,modular-frame
- Heavy Modular Frame,heavy-modular-frame
- Computer,computer
- Supercomputer,supercomputer
- Nuclear Pasta,nuclear-pasta
- Thermal Propulsion Rocket,thermal-propulsion-rocket
- Singularity Cell,singularity-cell

(You can open `data.json` and search for "name": "Item" to find exact key_name.)

## Planned / Future Features

- Production rates (/min) with integer machine counts (no fractional machines)
- LCM-based scaling for perfect balance
- Minimal machine mode (ceil at each step, accept overproduction)
- Miner / extractor counts (Mk.1–3, purity levels)
- Power consumption total
- Belt / pipe suggestions per stage
- Multiple simultaneous targets
- Export to JSON / simple factory layout text

## License
MIT – feel free to use, modify, share.
Made with frustration and love for Satisfactory factories.
