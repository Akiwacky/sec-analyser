from edgar import get_cik, get_company_facts
from utils import get_concept_data, to_annual_dataframe
import pandas as pd

def get_financials(ticker: str, years: int = 10) -> dict:
    """
    Pulls and cleans annual financial data for any ticker.
    Returns a dict of DataFrames, one per metric.
    """
    print(f"\nFetching data for {ticker}...")

    cik = get_cik(ticker)
    facts = get_company_facts(cik)
    us_gaap = facts['facts']['us-gaap']

    metrics = [
        "revenue",
        "net_income",
        "gross_profit",
        "operating_income",
        "total_assets",
        "total_liabilities",
        "equity",
        "operating_cashflow",
        "capex",
        "long_term_debt",
    ]

    results = {}

    for metric in metrics:
        try:
            data = get_concept_data(us_gaap, metric)
            df = to_annual_dataframe(data, years=years)
            results[metric] = df
            print(f"  ✓ {metric} — {len(df)} years")
        except ValueError:
            print(f"  ✗ {metric} — not found")
            results[metric] = None

    return results


def build_master_df(financials: dict) -> pd.DataFrame:
    """
    Combines all metric DataFrames into a single master DataFrame.
    Anchors on revenue years to exclude incomplete early rows.
    """
    master = None

    for metric, df in financials.items():
        if df is None:
            continue

        temp = df[['fiscal_year', 'val']].rename(
            columns={'val': metric}
        )

        if master is None:
            master = temp
        else:
            master = pd.merge(
                master, temp,
                on='fiscal_year',
                how='outer'
            )

    master = master.sort_values('fiscal_year').reset_index(drop=True)

    # Anchor to years where revenue exists
    # This removes early rows that only exist due to
    # long term debt or other metrics with deeper history
    master = master.dropna(subset=['revenue']).reset_index(drop=True)

    return master
# Run it
financials = get_financials("AAPL")
master = build_master_df(financials)

from ratios import calculate_ratios

# After building master df add:
ratios = calculate_ratios(master)

print("\nProfitability & Efficiency:")
print(ratios[[
    'fiscal_year',
    'gross_margin_%',
    'operating_margin_%', 
    'net_margin_%',
    'roe_%',
    'roa_%'
]].to_string(index=False))

print("\nGrowth:")
print(ratios[[
    'fiscal_year',
    'revenue_growth_%',
    'net_income_growth_%'
]].to_string(index=False))

print("\nLeverage:")
print(ratios[[
    'fiscal_year',
    'debt_to_equity',
    'debt_to_assets'
]].to_string(index=False))

print("\nCash Flow Quality:")
print(ratios[[
    'fiscal_year',
    'fcf_margin_%',
    'cash_conversion_%'
]].to_string(index=False))