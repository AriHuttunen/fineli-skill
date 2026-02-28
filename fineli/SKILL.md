---
name: fineli
description: "Look up food composition data from Fineli, Finland's national food composition database maintained by THL (Finnish Institute for Health and Welfare). Use this skill when the user asks about nutritional content of foods, macronutrients, micronutrients, or wants to compare foods nutritionally. Triggers include: 'how much protein in...', 'what are the macros for...', 'nutritional content of...', 'compare nutrition of X and Y', or any question about calories, carbs, fat, protein, vitamins, or minerals in a specific food."
---

# Fineli — Finnish Food Composition Database

## Requirements

**Network Access**: This skill requires network access to `fineli.fi`.

Add `fineli.fi` to **Additional allowed domains** in:
- **Claude Code**: Settings → Network → Additional allowed domains
- **Claude Desktop**: Settings → Network → Additional allowed domains

## Overview

Query food composition data from Fineli (fineli.fi), maintained by THL.
Data is licensed CC-BY 4.0 — always attribute: "Source: Finnish Institute for Health and Welfare, Fineli"

## Important: Always Let the User Choose

**Never auto-pick a food when multiple search results are returned.** Always present the numbered list to the user and ask them to choose. The only exception is when a search returns exactly one result.

## Workflow

**Always use `scripts/fineli.py`** (in this skill's directory).

### For macro questions ("how much protein in quinoa?")

1. Search:
   ```
   python3 scripts/fineli.py search "quinoa"
   ```
2. Present the numbered results to the user and ask which one they mean.
3. If only one result, you may proceed directly — the macros are already in the search output.
4. If the user wants more detail, use `detail` with the chosen ID.

### For micronutrient questions ("how much iron in quinoa?")

1. Search to find matching foods:
   ```
   python3 scripts/fineli.py search "quinoa"
   ```
2. Present the results and ask the user to pick one.
3. Get the specific nutrient for the chosen food:
   ```
   python3 scripts/fineli.py detail <id> --nutrient iron
   ```

### For comparisons ("compare oats and rice")

1. Search for the first food:
   ```
   python3 scripts/fineli.py search "oats"
   ```
2. Present results and ask the user to pick one.
3. Search for the second food:
   ```
   python3 scripts/fineli.py search "rice"
   ```
4. Present results and ask the user to pick one.
5. Compare using the two chosen IDs:
   ```
   python3 scripts/fineli.py compare <id1> <id2>
   ```

### Options

- `--lang fi|en|sv` — search language (default: en)
- `--top N` — number of search results to show (default: 5)
- `--nutrient NAME` — filter detail view to matching nutrients (substring match)

## Tips

- Finnish food names often work better than English for Finnish products (e.g. "ruisleipä" not "rye bread")
- Present values per 100 g unless the user asks for a specific portion size
