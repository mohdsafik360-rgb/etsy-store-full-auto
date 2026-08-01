# Etsy Digital Products Store

[![Stars](https://img.shields.io/github/stars/28AXE/etsy-store-full-auto?style=flat)](https://github.com/28AXE/etsy-store-full-auto)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

[![GitHub Topics](https://img.shields.io/badge/topics-etsy%20%7C%20digital--products%20%7C%20multi--agent%20%7C%20ai-blue)](https://github.com/28AXE/etsy-store-full-auto)

<p align="center">
  <strong>🤖 Autonomous multi-agent AI system for Etsy digital products</strong><br>
  Scrape competitors → Analyze gaps → Generate PDFs → Track performance
</p>

## Run in Google Colab ☁️

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/28AXE/etsy-store-full-auto/blob/master/etsy_store_colab.ipynb)

The fastest way to get started — no local setup required:

1. Open in Google Colab using the badge above or link below.
2. Add your **Gemini API key** in Colab Secrets (🔑 sidebar → `GEMINI_API_KEY`)
3. Run cells in order

> Get a free API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

## Architecture

4 agents, each powered by **Gemini API** for AI deliberation:

- **Scout** — Scrapes Etsy shops, extracts listing data (Playwright)
- **Analyst** — Identifies market opportunities and gaps (pandas + Gemini)
- **Creator** — Generates product content and PDFs (Gemini + reportlab)
- **Optimizer** — Tracks performance and recommends improvements (Gemini)

## Quick Start (Local)

```bash
# Install dependencies
uv sync
uv run playwright install chromium

# Set your Gemini API key
export GEMINI_API_KEY="your-api-key-here"

# Scrape a competitor shop
uv run etsy-store scrape "ShopName" -o data/shop.json

# Analyze market data
uv run etsy-store analyze data/shop.json

# Generate a digital product
uv run etsy-store generate "Daily Planner" -o output
```

## Project Structure

```
etsy-store/
├── scout/          # Scraping agent (Playwright + BeautifulSoup)
├── analyst/        # Market analysis agent (pandas + Gemini)
├── creator/        # Content generation agent (Gemini + PDF)
├── optimizer/      # Performance tracking agent (analytics + Gemini)
├── config/         # Configuration files (niches, pricing)
├── gemini_client.py  # Unified Gemini API wrapper
├── etsy_store_colab.ipynb  # Google Colab notebook
├── data/           # Scraped data and analytics
├── docs/           # Documentation
└── tests/          # Test suite
```

## Requirements

- Python 3.10+
- uv (package manager) — for local usage
- Gemini API key ([get one free](https://aistudio.google.com/apikey))
- Playwright browsers

## License

MIT
