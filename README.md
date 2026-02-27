# Fineli Skill for Claude Code

A Claude Code skill for querying nutritional data from [Fineli](https://fineli.fi), Finland's national food composition database maintained by THL (Finnish Institute for Health and Welfare).

## What It Does

This skill enables Claude Code to answer questions about food nutrition by querying the Fineli API. It can:

- Look up macronutrients (protein, fat, carbohydrates, fiber, calories) for any food
- Retrieve detailed micronutrient data (vitamins, minerals, fatty acids)
- Compare nutritional content across different foods
- Handle Finnish, English, and Swedish food names
- Identify special diet suitability (gluten-free, vegan, lactose-free, etc.)

All nutritional values are per 100g edible portion.

## Setup

### Network Access Required

Add `fineli.fi` to **Additional allowed domains** in:
- **Claude Code**: Settings → Network → Additional allowed domains
- **Claude Desktop**: Settings → Network → Additional allowed domains

### Installation

Copy `SKILL.md` and `components-mapping.json` to your Claude Code skills directory.

## Data Source

All data comes from the Fineli database, licensed under CC-BY 4.0.

**Attribution**: Source: Finnish Institute for Health and Welfare, Fineli

## Example Queries

- "How much protein is in quinoa?"
- "What are the macros for salmon?"
- "Compare the nutritional content of oats and rice"
- "How much vitamin D is in milk?"

## Disclaimer

**This tool is provided as-is with no guarantees of accuracy or correctness.** Nutritional data is retrieved from the Fineli database and may contain errors, be outdated, or be misinterpreted. Always verify critical nutritional information with authoritative sources. The authors assume no liability for decisions made based on this data.

## Files

- `SKILL.md` — Skill specification and API documentation
- `components-mapping.json` — Maps Fineli's nutrient array positions to human-readable names
