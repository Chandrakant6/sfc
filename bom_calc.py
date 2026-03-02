# bom_calculator.py - Satisfactory Bill of Materials Tree (Single Standard Recipe)
import json
from collections import defaultdict

def load_recipes(json_path='data.json'):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: '{json_path}' not found.")
        print("Download from: https://raw.githubusercontent.com/KirkMcDonald/satisfactory-calculator/master/data/data.json")
        print("Save as 'data.json' in the same folder.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in data.json - probably saved HTML instead of raw data.")
        exit(1)

    cat_to_name = {b['category']: b['name'] for b in data['buildings']}

    recipes = {}
    for r in data['recipes']:
        cat = r['category']
        if cat not in cat_to_name:
            continue
        recipes[r['key_name']] = {
            'name': r['name'],
            'ingredients': {ing[0]: ing[1] for ing in r['ingredients']},
            'products': {p[0]: p[1] for p in r['products']},
            'producer': cat_to_name.get(cat, 'Unknown')
        }
    return recipes


def select_standard_recipes(recipes):
    # Items that should NEVER have a crafting recipe (must be mined/extracted)
    raw_resources = {
        'iron-ore', 'copper-ore', 'limestone', 'coal', 'caterium-ore',
        'raw-quartz', 'sulfur', 'bauxite', 'uranium', 'sam-ore',
        'crude-oil', 'water', 'nitrogen-gas'
    }

    defaults = {}

    alt_keywords = [
        'alternate', 'alt:', 'sloppy', 'pure', 'infused', 'bolted',
        'stamped', 'wet', 'compacted', 'quickened', 'steamed', 'recycled',
        'reanimated', 'limestone', '(limestone)'
    ]

    for key, rec in recipes.items():
        lower_name = rec['name'].lower()
        if any(kw in lower_name for kw in alt_keywords):
            continue

        # We take the first product as primary
        primary = next(iter(rec['products']), None)
        if primary is None:
            continue

        # Skip if it's a raw resource being "produced" by some weird recipe
        if primary in raw_resources:
            continue

        # Prefer exact name match and simple recipes
        if primary not in defaults or len(rec['ingredients']) == 1:
            defaults[primary] = key

    # Hard overrides - force standard recipes only
    forced = {
        'iron-ingot': 'iron-ingot',
        'copper-ingot': 'copper-ingot',
        'iron-rod': 'iron-rod',
        'screw': 'screw',
        'iron-plate': 'iron-plate',
        'reinforced-iron-plate': 'reinforced-iron-plate',
        'rotor': 'rotor',
        'stator': 'stator',
        'motor': 'motor',
        'circuit-board': 'circuit-board',
        'plastic': 'plastic',
        'rubber': 'rubber',
        'modular-frame': 'modular-frame',
        'heavy-modular-frame': 'heavy-modular-frame',
        'computer': 'computer',
    }

    for item, rec_key in forced.items():
        if rec_key in recipes:
            defaults[item] = rec_key

    # Never allow recipes for raw resources
    for raw in raw_resources:
        defaults.pop(raw, None)

    return defaults


def print_bom_tree(item, recipes, defaults, prefix="", path=None):
    if path is None:
        path = set()

    if item in path:
        print(prefix + "└── " + item + "  (CYCLE DETECTED!)")
        return

    if item not in defaults:
        print(prefix + "└── " + item + "  (RAW RESOURCE – mine / extract)")
        return

    path.add(item)
    rec_key = defaults[item]
    rec = recipes[rec_key]

    print(prefix + "└── " + item + "  [" + rec['name'] + " – " + rec['producer'] + "]")

    ingredients = sorted(rec['ingredients'].items(), key=lambda x: x[1], reverse=True)

    for i, (ing_item, qty) in enumerate(ingredients):
        last = i == len(ingredients) - 1
        new_prefix = prefix + ("    " if last else "│   ")
        print(new_prefix + "└── " + f"{qty:g}" + " × " + ing_item)
        print_bom_tree(ing_item, recipes, defaults, new_prefix + "    ", path.copy())

    path.remove(item)


def main():
    print("=== Satisfactory BOM Tree (Standard Recipes Only) ===\n")
    print("Shows what items + recipes are needed to produce 1 unit of your target.\n")

    recipes = load_recipes()
    defaults = select_standard_recipes(recipes)

    while True:
        target = input("Target item (e.g. rotor, plastic, motor, computer) or 'quit': ").strip().lower()
        if target in ('quit', 'q', 'exit', ''):
            if target == '':
                target = 'rotor'
            else:
                print("Goodbye!")
                break

        print(f"\n┌── Required to produce 1 × {target.replace('-', ' ').title()}")
        print_bom_tree(target, recipes, defaults)
        print("\n" + "─" * 70 + "\n")


if __name__ == "__main__":
    main()
