# Agno Zenrows Live Web Agent

## Description

This project uses two Agno agents to retrieve current web data through [Zenrows Fetch](https://www.zenrows.com/products/scraper-api) and turn the returned content into a structured market snapshot. The web data agent handles live web access, while the processing agent extracts only values supported by the fetched page.

## Features

- Registers Zenrows Fetch as a typed Python tool in Agno
- Uses a deterministic two-agent handoff
- Compares a direct request with the response returned by Fetch
- Uses `mode=auto` to select the access configuration for each target
- Returns a validated Pydantic result
- Keeps API credentials in environment variables
- Includes isolated tests that do not spend API credits

## Prerequisites

- Python 3.11, 3.12, or 3.13
- A [Zenrows API key](https://app.zenrows.com/register)
- An OpenAI API key

Use only public pages you are authorized to access. Do not use this project to collect personal data or access restricted categories of sites.

## Installation

```bash
git clone https://github.com/Tiioluwani/agno-zenrows-live-web-agent.git
cd agno-zenrows-live-web-agent

python -m venv .venv
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuration

Copy the example environment file and replace the placeholder values:

```bash
cp .env.example .env
```

```env
ZENROWS_API_KEY=replace_with_your_zenrows_api_key
OPENAI_API_KEY=replace_with_your_openai_api_key
OPENAI_MODEL=gpt-5-mini
TARGET_URL=https://www.scrapingcourse.com/javascript-rendering
```

## Project Structure

```text
agno-zenrows-live-web-agent/
├── src/live_web_agent/
│   ├── agents.py
│   ├── cli.py
│   ├── config.py
│   ├── schemas.py
│   ├── web.py
│   └── workflow.py
├── tests/
├── .env.example
├── .gitignore
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── VALIDATION.md
└── README.md
```

## How It Works

1. The CLI optionally sends a normal HTTP request to make the access difference visible.
2. The web data agent calls `fetch_with_zenrows()` with `mode=auto`.
3. Fetch selects the access configuration for the target before returning the page content.
4. The tool removes scripts and styles, preserves relevant market metadata, and limits the page text before returning it to the agent.
5. The workflow passes the validated `FetchedPage` object to the market intelligence agent.
6. The second agent returns a validated `MarketSnapshot` with evidence from the page.

## Running the Project

Run the configured target:

```bash
live-web-agent
```

Run the separately validated Cloudflare challenge target:

```bash
live-web-agent --url "https://www.scrapingcourse.com/cloudflare-challenge"
```

Skip the direct-request comparison:

```bash
live-web-agent --skip-direct
```

Run the tests:

```bash
pytest -q
ruff check .
```

## Output

Two scenarios were validated on September 19, 2026:

1. **Cloudflare challenge:** the direct request returned HTTP `403` with `Just a moment...`. Zenrows returned HTTP `200` with content containing `You bypassed the Cloudflare challenge! :D`.
2. **JavaScript-rendered products:** the direct request returned HTTP `200`, but its HTML contained no populated product names or prices. The Zenrows response contained 12 populated products. The two-agent workflow selected one product and produced the `MarketSnapshot` below.

This is the genuine structured output printed by the September 19, 2026 validation run:

```json
{
  "product_name": "Chaz Kangeroo Hoodie",
  "current_price": 52.0,
  "currency": "USD",
  "availability": "http://schema.org/InStock",
  "source_url": "https://www.scrapingcourse.com/javascript-rendering",
  "collected_at": "2026-09-19T02:03:50.564253Z",
  "evidence": [
    "Chaz Kangeroo Hoodie $52",
    "priceCurrency: USD",
    "availability: http://schema.org/InStock"
  ]
}
```

The CLI did not expose Zenrows credit usage, so no credit figure is claimed.

## Technologies

- Python
- Agno
- Zenrows Fetch
- OpenAI
- Pydantic
- Requests
- Beautiful Soup
- Pytest

## Related Article

Article URL to be added after publication.
