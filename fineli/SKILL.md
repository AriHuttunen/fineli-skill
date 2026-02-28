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

## Workflow

**Always use `scripts/fineli.py`** (in this skill's directory) instead of calling the API directly.
The script handles all API requests, JSON parsing, and formatting.

### For macro questions ("how much protein in quinoa?")

```
python3 scripts/fineli.py search "quinoa"
```

Pick the best match from the output and present the relevant values.
Prefer raw/unprocessed items for ingredients, cooked items if the user specifies.

### For micronutrient questions ("how much iron in quinoa?")

1. Search to find the food ID:
   ```
   python3 scripts/fineli.py search "quinoa"
   ```
2. Get the specific nutrient:
   ```
   python3 scripts/fineli.py detail <id> --nutrient iron
   ```

### For comparisons ("compare oats and rice")

```
python3 scripts/fineli.py compare "oats" "rice"
```

### Options

- `--lang fi|en|sv` — search language (default: en)
- `--top N` — number of search results to show (default: 5)
- `--nutrient NAME` — filter detail view to matching nutrients (substring match)

## Tips

- Finnish food names often work better than English for Finnish products (e.g. "ruisleipä" not "rye bread")
- Present values per 100 g unless the user asks for a specific portion size
