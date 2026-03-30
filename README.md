# SEC Financial Analyser

A Python tool that pulls financial data directly from the
SEC EDGAR API and generates key financial ratios for any
US-listed company.

## What it does

- Fetches 10-K annual filing data via SEC EDGAR XBRL API
- Handles concept mapping across different XBRL tag names
- Cleans and structures 10 years of financial history
- Calculates profitability, growth, leverage and cash flow ratios

## Metrics tracked

- Revenue, Net Income, Gross Profit, Operating Income
- Total Assets, Liabilities, Equity
- Operating Cash Flow, CapEx, Free Cash Flow
- Long Term Debt

## Ratios calculated

- Gross, Operating and Net Margins
- ROE, ROA
- Revenue and Net Income Growth (YoY)
- Debt/Equity, Debt/Assets
- FCF Margin, Cash Conversion

## Data source

SEC EDGAR XBRL API — https://data.sec.gov

## Roadmap

- [ ] Visualisation layer (matplotlib/plotly)
- [ ] PDF/HTML report output
- [ ] Streamlit UI
- [ ] Peer comparison
- [ ] Macro dashboard (World Bank / IMF API)
