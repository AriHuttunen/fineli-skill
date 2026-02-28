# Fineli Skill for Claude

Look up nutritional data from [Fineli](https://fineli.fi), Finland's national food composition database maintained by THL (Finnish Institute for Health and Welfare) — directly from Claude.

Ask things like "how much protein in quinoa?", "compare oats and rice", or "how much vitamin D is in milk?" and get accurate data from Fineli without leaving the conversation.

## Skill files

The installable skill lives in the `fineli/` subdirectory:

```
fineli/
├── SKILL.md          # Skill instructions
└── scripts/
    └── fineli.py     # API query script (Python 3, stdlib only)
```

## Setup

### 1. Install the skill

Download or clone this repo, then zip and upload the `fineli/` subdirectory manually:

1. Zip the `fineli/` folder
2. Open Claude.ai → Settings → Capabilities → Skills
3. Upload the zip

For Claude Code, copy the `fineli/` folder to your skills directory instead.

### 2. Allow network access

Add `fineli.fi` to **Additional allowed domains** in your Claude settings (Settings > Network).

## Requirements

Python 3 (stdlib only — no pip dependencies needed).

## Data Source

All data comes from the Fineli database, licensed under CC-BY 4.0.

**Attribution**: Source: Finnish Institute for Health and Welfare, Fineli

## Disclaimer

This tool is provided as-is with no guarantees of accuracy or correctness. Nutritional data is retrieved from the Fineli database and may contain errors, be outdated, or be misinterpreted. Always verify critical nutritional information with authoritative sources.

## License

See [LICENSE](LICENSE).
