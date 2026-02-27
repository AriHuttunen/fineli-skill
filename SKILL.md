---
name: fineli
description: "Look up food composition data from Fineli, Finland's national food composition database maintained by THL (Finnish Institute for Health and Welfare). Use this skill when the user asks about nutritional content of foods, macronutrients, micronutrients, or wants to compare foods nutritionally. Triggers include: 'how much protein in...', 'what are the macros for...', 'nutritional content of...', 'compare nutrition of X and Y', or any question about calories, carbs, fat, protein, vitamins, or minerals in a specific food."
---

# Fineli — Finnish Food Composition Database

## ⚠️ Requirements

**Network Access**: This skill requires network access to `fineli.fi`.

Add `fineli.fi` to **Additional allowed domains** in:
- **Claude Code**: Settings → Network → Additional allowed domains
- **Claude Desktop**: Settings → Network → Additional allowed domains

## Overview

Query food composition data from Fineli (fineli.fi), maintained by THL.
Data is licensed CC-BY 4.0 — always attribute: "Source: Finnish Institute for Health and Welfare, Fineli"

## API Endpoints

### 1. Search foods by name (primary tool)

```
GET https://fineli.fi/fineli/api/v1/foods?q={search_term}&lang=en
```

- `q`: search term (supports Finnish or English names)
- `lang`: `en`, `fi`, or `sv`
- Returns JSON array of matching foods with **macros included directly**:
  `fat`, `protein`, `carbohydrate`, `fiber`, `sugar`, `saturatedFat`,
  `energy` (kJ), `energyKcal`, `salt`, `alcohol`, `organicAcids`, `sugarAlcohol`
- Also returns: `id`, `name` (fi/sv/en/la), `preparationMethod`, `specialDiets`, `units` (portion sizes with gram weights)
- All values are per 100 g

**This endpoint is sufficient for most macro lookups.** No further calls needed.

### 2. Get full nutrient detail by food ID

```
GET https://fineli.fi/fineli/api/v1/foods/{id}
```

- Returns everything from the search endpoint PLUS a `data` array with all 55 nutrient values
- The `data` array is positional — use the mapping in `components-mapping.json` to decode it
- Use this only when the user needs **micronutrients** (vitamins, minerals, fatty acid detail)

### 3. List all nutrient components (reference only)

```
GET https://fineli.fi/fineli/api/v1/components?lang=en
```

- Returns descriptions and units for all 55 tracked nutrients
- Rarely needed — the static mapping file covers this

## Workflow

### For macro questions ("how much protein in quinoa?")

1. `curl -s "https://fineli.fi/fineli/api/v1/foods?q=quinoa&lang=en"` 
2. Pick the best match (prefer raw/unprocessed items for ingredients, cooked items if user specifies)
3. Present macros from the response fields directly

### For micronutrient questions ("how much iron in quinoa?")

1. Search as above to find the food ID
2. `curl -s "https://fineli.fi/fineli/api/v1/foods/{id}"`
3. Read the `data` array and map positions using `components-mapping.json`

### For comparisons ("compare quinoa and rice")

1. Search for each food
2. Present side by side

## Tips

- Finnish food names often work better than English for Finnish products (e.g. "ruisleipä" not "rye bread")
- Multiple results are common — look at `preparationMethod` to distinguish raw vs cooked vs fried
- The `units` array gives Finnish portion sizes (dl, pieni/keskikokoinen/iso annos) with gram weights
- `specialDiets` indicates suitability: GLUTFREE, VEGAN, LACSFREE, MILKFREE, etc.
- Energy is in kJ (field `energy`) and kcal (field `energyKcal`). Present kJ as primary with kcal in parentheses, following Finnish convention.
- Salt values in the search response are in mg. On the Fineli website they display as mg.
- Present values per 100 g unless the user asks for a specific portion size, in which case calculate using the `units` mass values.
