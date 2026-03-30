import requests

# EDGAR requires a User-Agent header identifying yourself
# Without it your requests will eventually get blocked
HEADERS = {
    "User-Agent": "Tim Morant 	morantt72@gmail.com"
}

def get_cik(ticker: str) -> str:
    """
    Converts a stock ticker to an SEC CIK number.

    Args:
        ticker: Stock ticker e.g. "AAPL"

    Returns:
        CIK as a zero-padded 10-digit string e.g. "0000320193"
    """
    url = "https://www.sec.gov/files/company_tickers.json"

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  # Raises an error if the request fails

    data = response.json()

    ticker = ticker.upper()

    for entry in data.values():
        if entry["ticker"] == ticker:
            return str(entry["cik_str"]).zfill(10)

    raise ValueError(f"Ticker {ticker} not found in EDGAR database")

def get_company_facts(cik: str) -> dict:
    """
    Pulls all reported financial facts for a company from EDGAR.

    Args:
        cik: Zero-padded 10-digit CIK e.g. "0000320193"

    Returns:
        Raw JSON dict containing all financial facts across all filings
    """
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    return response.json()