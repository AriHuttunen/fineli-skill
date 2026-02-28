#!/usr/bin/env python3
"""Fineli food composition database CLI helper.

Queries the Fineli API (fineli.fi) and outputs formatted nutritional data.
Uses only Python stdlib — no pip dependencies.
"""

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://fineli.fi/fineli/api/v1"
DEFAULT_LANG = "en"
DEFAULT_TOP = 5
ATTRIBUTION = "Source: Finnish Institute for Health and Welfare, Fineli"

# Nutrient component mapping — positional index in the /foods/{id} data array.
# Verified against fineli.fi. See components-mapping.json for reference.
COMPONENTS = [
    (0,  "Energy",                              "kJ",  "macro"),
    (1,  "Fat, total",                          "g",   "macro"),
    (2,  "Carbohydrate, available",             "g",   "macro"),
    (3,  "Protein, total",                      "g",   "macro"),
    (4,  "Alcohol",                             "g",   "macro"),
    (5,  "Organic acids, total",                "g",   "macro"),
    (6,  "Sugar alcohols",                      "g",   "carbohydrate"),
    (7,  "Sugars, total",                       "g",   "carbohydrate"),
    (8,  "Fructose",                            "g",   "carbohydrate"),
    (9,  "Galactose",                           "g",   "carbohydrate"),
    (10, "Glucose",                             "g",   "carbohydrate"),
    (11, "Lactose",                             "g",   "carbohydrate"),
    (12, "Maltose",                             "g",   "carbohydrate"),
    (13, "Sucrose",                             "g",   "carbohydrate"),
    (14, "Starch, total",                       "g",   "carbohydrate"),
    (15, "Fibre, total",                        "g",   "carbohydrate"),
    (16, "Fibre, water-insoluble",              "g",   "carbohydrate"),
    (17, "Polysaccharides, soluble",            "g",   "carbohydrate"),
    (18, "Fatty acids, total",                  "g",   "fat"),
    (19, "Fatty acids, polyunsaturated (PUFA)", "g",   "fat"),
    (20, "Fatty acids, monounsaturated (MUFA)", "g",   "fat"),
    (21, "Fatty acids, saturated (SAFA)",       "g",   "fat"),
    (22, "Fatty acids, trans",                  "g",   "fat"),
    (23, "Fatty acids, n-3 polyunsaturated",    "g",   "fat"),
    (24, "Fatty acids, n-6 polyunsaturated",    "g",   "fat"),
    (25, "Linoleic acid (18:2 n-6)",            "mg",  "fat"),
    (26, "Alpha-linolenic acid (18:3 n-3)",     "mg",  "fat"),
    (27, "EPA (20:5 n-3)",                      "mg",  "fat"),
    (28, "DHA (22:6 n-3)",                      "mg",  "fat"),
    (29, "Cholesterol",                         "mg",  "fat"),
    (30, "Sterols, total",                      "mg",  "fat"),
    (31, "Calcium",                             "mg",  "mineral"),
    (32, "Iron, total",                         "mg",  "mineral"),
    (33, "Iodide",                              "µg",  "mineral"),
    (34, "Potassium",                           "mg",  "mineral"),
    (35, "Magnesium",                           "mg",  "mineral"),
    (36, "Sodium",                              "mg",  "mineral"),
    (37, "Salt",                                "mg",  "mineral"),
    (38, "Phosphorus",                          "mg",  "mineral"),
    (39, "Selenium",                            "µg",  "mineral"),
    (40, "Zinc",                                "mg",  "mineral"),
    (41, "Tryptophan",                          "mg",  "amino_acid"),
    (42, "Folate, total",                       "µg",  "vitamin"),
    (43, "Niacin equivalents",                  "mg",  "vitamin"),
    (44, "Niacin",                              "mg",  "vitamin"),
    (45, "Vitamin B6 (pyridoxine)",             "mg",  "vitamin"),
    (46, "Riboflavin (B2)",                     "mg",  "vitamin"),
    (47, "Thiamin (B1)",                        "mg",  "vitamin"),
    (48, "Vitamin A (RAE)",                     "µg",  "vitamin"),
    (49, "Carotenoids, total",                  "µg",  "vitamin"),
    (50, "Vitamin B12 (cobalamin)",             "µg",  "vitamin"),
    (51, "Vitamin D",                           "µg",  "vitamin"),
    (52, "Vitamin C",                           "mg",  "vitamin"),
    (53, "Vitamin E (alpha-tocopherol)",        "mg",  "vitamin"),
    (54, "Vitamin K",                           "µg",  "vitamin"),
]

COMPONENT_BY_INDEX = {c[0]: c for c in COMPONENTS}
COMPONENT_BY_NAME = {c[1].lower(): c for c in COMPONENTS}

CATEGORY_LABELS = {
    "macro": "Macronutrients",
    "carbohydrate": "Carbohydrate Detail",
    "fat": "Fat Detail",
    "mineral": "Minerals",
    "vitamin": "Vitamins",
    "amino_acid": "Amino Acids",
}

CATEGORY_ORDER = ["macro", "carbohydrate", "fat", "mineral", "vitamin", "amino_acid"]

DIET_LABELS = {
    "GLUTFREE": "gluten-free",
    "VEGAN": "vegan",
    "LACSFREE": "lactose-free",
    "MILKFREE": "milk-free",
    "EGGFREE": "egg-free",
    "SOYFREE": "soy-free",
}


# ── API layer ────────────────────────────────────────────────────────────────


def api_get(path, params=None):
    """GET request to Fineli API. Returns parsed JSON."""
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "fineli-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: Not found ({url}).", file=sys.stderr)
        else:
            print(f"Error: Fineli API returned HTTP {e.code}.", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(
            f"Error: Could not connect to fineli.fi ({e.reason}).\n"
            "Check your network and that fineli.fi is in allowed domains.",
            file=sys.stderr,
        )
        sys.exit(1)


def search_foods(term, lang=DEFAULT_LANG):
    return api_get("/foods", {"q": term, "lang": lang})


def get_food_detail(food_id):
    return api_get(f"/foods/{food_id}")


# ── Helpers ──────────────────────────────────────────────────────────────────


def food_name(food, lang=DEFAULT_LANG):
    name_obj = food.get("name", {})
    return name_obj.get(lang) or name_obj.get("en") or name_obj.get("fi") or "Unknown"


def fmt(value, unit):
    """Format a numeric value with its unit."""
    if value is None:
        return "—"
    return f"{value:.1f} {unit}"


def diets_str(food):
    diets = food.get("specialDiets", [])
    labels = [DIET_LABELS[d] for d in diets if d in DIET_LABELS]
    return ", ".join(labels) if labels else ""


def prep_str(food):
    pm_list = food.get("preparationMethod", [])
    if not pm_list:
        return ""
    pm = pm_list[0]
    desc = pm.get("abbreviation") or pm.get("description") or {}
    return desc.get("en") or desc.get("fi") or ""


# ── Formatting ───────────────────────────────────────────────────────────────


def format_macro_block(food, lang=DEFAULT_LANG, indent="   "):
    """Format a single food's macros as a readable block."""
    lines = []
    name = food_name(food, lang)
    prep = prep_str(food)
    diets = diets_str(food)

    meta_parts = []
    if prep:
        meta_parts.append(f"Preparation: {prep}")
    if diets:
        meta_parts.append(f"Diets: {diets}")
    if meta_parts:
        lines.append(f"{indent}{' | '.join(meta_parts)}")

    energy_kj = food.get("energy")
    energy_kcal = food.get("energyKcal")
    lines.append(f"{indent}{'Energy:':<14} {fmt(energy_kj, 'kJ'):<12} ({fmt(energy_kcal, 'kcal')})")
    lines.append(f"{indent}{'Protein:':<14} {fmt(food.get('protein'), 'g')}")
    lines.append(f"{indent}{'Fat:':<14} {fmt(food.get('fat'), 'g')}")
    lines.append(f"{indent}{'  Saturated:':<14} {fmt(food.get('saturatedFat'), 'g')}")
    lines.append(f"{indent}{'Carbs:':<14} {fmt(food.get('carbohydrate'), 'g')}")
    lines.append(f"{indent}{'  Sugar:':<14} {fmt(food.get('sugar'), 'g')}")
    lines.append(f"{indent}{'  Fiber:':<14} {fmt(food.get('fiber'), 'g')}")
    lines.append(f"{indent}{'Salt:':<14} {fmt(food.get('salt'), 'mg')}")
    return "\n".join(lines)


def format_search_results(foods, lang, top):
    if not foods:
        return None
    shown = foods[:top]
    lines = [
        f'Fineli search results (top {len(shown)} of {len(foods)})',
        "All values per 100 g.",
        "",
    ]
    for i, food in enumerate(shown, 1):
        fid = food.get("id", "?")
        name = food_name(food, lang)
        lines.append(f"{i}. {name} (id: {fid})")
        lines.append(format_macro_block(food, lang))
        lines.append("")
    lines.append(ATTRIBUTION)
    return "\n".join(lines)


def format_nutrient_profile(food, lang=DEFAULT_LANG, nutrient_filter=None):
    data = food.get("data")
    if data is None:
        return "Error: No nutrient data in response."

    name = food_name(food, lang)
    fid = food.get("id", "?")
    prep = prep_str(food)

    # If filtering to a specific nutrient
    if nutrient_filter:
        query = nutrient_filter.lower()
        matches = [(c, data[c[0]]) for c in COMPONENTS
                   if query in c[1].lower() and c[0] < len(data)]
        if not matches:
            names = [c[1] for c in COMPONENTS]
            return (
                f'Nutrient "{nutrient_filter}" not found.\n'
                f"Available nutrients:\n" + "\n".join(f"  - {n}" for n in names)
            )
        lines = [f"{name} (id: {fid})", f"All values per 100 g.", ""]
        for comp, val in matches:
            lines.append(f"  {comp[1]:<40} {fmt(val, comp[2]):>12}")
        lines.append("")
        lines.append(ATTRIBUTION)
        return "\n".join(lines)

    # Full profile grouped by category
    lines = [
        f"{name} (id: {fid})",
        f"Preparation: {prep}" if prep else None,
        "All values per 100 g.",
        "",
    ]
    lines = [l for l in lines if l is not None]

    for cat in CATEGORY_ORDER:
        cat_components = [c for c in COMPONENTS if c[3] == cat and c[0] < len(data)]
        if not cat_components:
            continue
        lines.append(f"── {CATEGORY_LABELS[cat]} ──")
        for comp in cat_components:
            val = data[comp[0]]
            lines.append(f"  {comp[1]:<40} {fmt(val, comp[2]):>12}")
        lines.append("")

    lines.append(ATTRIBUTION)
    return "\n".join(lines)


def format_comparison(term1, food1, term2, food2, lang=DEFAULT_LANG):
    name1 = food_name(food1, lang)
    name2 = food_name(food2, lang)

    # Truncate long names for column headers
    col1 = name1[:20] + "…" if len(name1) > 20 else name1
    col2 = name2[:20] + "…" if len(name2) > 20 else name2

    lines = [
        f"Comparison: {name1} vs {name2}",
        f'Selected: "{name1}" for "{term1}", "{name2}" for "{term2}"',
        "All values per 100 g.",
        "",
        f"  {'Nutrient':<24} {col1:>20} {col2:>20}",
        "  " + "─" * 64,
    ]

    rows = [
        ("Energy (kJ)",    food1.get("energy"),       food2.get("energy"),       ""),
        ("Energy (kcal)",  food1.get("energyKcal"),   food2.get("energyKcal"),   ""),
        ("Protein",        food1.get("protein"),       food2.get("protein"),      "g"),
        ("Fat",            food1.get("fat"),           food2.get("fat"),          "g"),
        ("  Saturated",    food1.get("saturatedFat"),  food2.get("saturatedFat"), "g"),
        ("Carbohydrate",   food1.get("carbohydrate"),  food2.get("carbohydrate"),"g"),
        ("  Sugar",        food1.get("sugar"),          food2.get("sugar"),       "g"),
        ("  Fiber",        food1.get("fiber"),          food2.get("fiber"),       "g"),
        ("Salt (mg)",      food1.get("salt"),           food2.get("salt"),        ""),
    ]

    for label, v1, v2, unit in rows:
        s1 = f"{v1:.1f}" if v1 is not None else "—"
        s2 = f"{v2:.1f}" if v2 is not None else "—"
        if unit:
            s1 = f"{s1} {unit}" if v1 is not None else s1
            s2 = f"{s2} {unit}" if v2 is not None else s2
        lines.append(f"  {label:<24} {s1:>20} {s2:>20}")

    lines.append("")
    lines.append(ATTRIBUTION)
    return "\n".join(lines)


# ── Commands ─────────────────────────────────────────────────────────────────


def cmd_search(args):
    foods = search_foods(args.term, args.lang)
    if not foods:
        print(f'No results found for "{args.term}". Try a different spelling or a Finnish name.')
        return
    print(format_search_results(foods, args.lang, args.top))


def cmd_detail(args):
    food = get_food_detail(args.id)
    print(format_nutrient_profile(food, args.lang, args.nutrient))


def cmd_compare(args):
    foods1 = search_foods(args.term1, args.lang)
    foods2 = search_foods(args.term2, args.lang)

    if not foods1:
        print(f'No results found for "{args.term1}".', file=sys.stderr)
        sys.exit(1)
    if not foods2:
        print(f'No results found for "{args.term2}".', file=sys.stderr)
        sys.exit(1)

    print(format_comparison(args.term1, foods1[0], args.term2, foods2[0], args.lang))


# ── CLI ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Query Fineli food composition data.")
    parser.add_argument("--lang", default=DEFAULT_LANG, choices=["en", "fi", "sv"])
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="Search foods by name")
    p_search.add_argument("term")
    p_search.add_argument("--top", type=int, default=DEFAULT_TOP)
    p_search.set_defaults(func=cmd_search)

    p_detail = sub.add_parser("detail", help="Full nutrient profile by food ID")
    p_detail.add_argument("id", type=int)
    p_detail.add_argument("--nutrient", help="Filter to a specific nutrient (substring match)")
    p_detail.set_defaults(func=cmd_detail)

    p_compare = sub.add_parser("compare", help="Compare two foods side by side")
    p_compare.add_argument("term1")
    p_compare.add_argument("term2")
    p_compare.set_defaults(func=cmd_compare)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
