# Validation record

## Completed validation

- Date: September 19, 2026
- Python: 3.12.14
- Agno: 3.0.10
- Automated tests: 20 passed
- Ruff: all checks passed
- Agno initialization: both agents instantiated successfully with their expected output schemas

### Cloudflare challenge

- Target: `https://www.scrapingcourse.com/cloudflare-challenge`
- Direct request: HTTP 403 with `Just a moment...`
- Zenrows request: HTTP 200 with `You bypassed the Cloudflare challenge! :D`

### JavaScript-rendered products

- Target: `https://www.scrapingcourse.com/javascript-rendering`
- Direct request: HTTP 200, but product names and prices were empty
- Zenrows request: 12 populated products after JavaScript rendering and a five-second wait
- Both agents completed successfully
- Final `MarketSnapshot`:

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

- Zenrows credit usage: not exposed by the command
- Remaining runtime errors: none
