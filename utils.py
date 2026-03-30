import pandas as pd

# Priority-ordered concept names for each metric
# We try each one in order and use the first one that exists
# This handles the fact that companies use different XBRL tags

CONCEPT_MAP = {
   "revenue": [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "Revenues",
    "SalesRevenueNet",
    "SalesRevenueGoodsNet",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "SalesRevenueServicesNet",
    "RevenueFromContractWithCustomer",
],
    "net_income": [
        "NetIncomeLoss",
        "ProfitLoss",
        "NetIncomeLossAvailableToCommonStockholdersBasic",
    ],
    "gross_profit": [
        "GrossProfit",
    ],
    "operating_income": [
        "OperatingIncomeLoss",
    ],
    "total_assets": [
        "Assets",
    ],
    "total_liabilities": [
        "Liabilities",
    ],
    "equity": [
        "StockholdersEquity",
        "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
    ],
    "operating_cashflow": [
        "NetCashProvidedByUsedInOperatingActivities",
    ],
    "capex": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
    ],
    "long_term_debt": [
        "LongTermDebt",
        "LongTermDebtNoncurrent",
    ],
    "rd_expense": [
        "ResearchAndDevelopmentExpense",
    ],
}


def get_concept_data(us_gaap: dict, metric: str) -> list:
    """
    Tries each concept name for a metric in priority order.
    Returns the first one that exists in the company's filings.

    Args:
        us_gaap: The us-gaap facts dict from EDGAR
        metric: Key from CONCEPT_MAP e.g. "revenue"

    Returns:
        List of reported values for that concept

    Raises:
        ValueError if none of the concept names are found
    """
    concepts = CONCEPT_MAP.get(metric)

    if not concepts:
        raise ValueError(f"Unknown metric: {metric}")

    for concept in concepts:
        if concept in us_gaap:
            data = us_gaap[concept].get("units", {}).get("USD", [])
            if data:
                return data

    raise ValueError(
        f"Could not find data for metric '{metric}' "
        f"in any of these concepts: {concepts}"
    )


def to_annual_dataframe(data: list, years: int = 10) -> pd.DataFrame:
    """
    Filters raw EDGAR concept data to clean annual 10-K figures.
    
    Args:
        data: Raw list of entries from EDGAR
        years: How many years of history to return (default 10)
    """
    df = pd.DataFrame(data)

    df = df[
        (df['form'] == '10-K') &
        (df['fp'] == 'FY')
    ].copy()

    df['end'] = pd.to_datetime(df['end'])
    df['filed'] = pd.to_datetime(df['filed'])

    if 'start' in df.columns:
        df['start'] = pd.to_datetime(df['start'])
        df['period_days'] = (df['end'] - df['start']).dt.days
        df = df[
            (df['period_days'] >= 340) &
            (df['period_days'] <= 390)
        ].copy()

    df['fiscal_year'] = df['end'].dt.year

    df = (
        df.sort_values('filed')
          .drop_duplicates(subset=['fiscal_year'], keep='last')
    )

    df = df.sort_values('end').reset_index(drop=True)

    df = df[['fiscal_year', 'end', 'val', 'filed']]
    df['val_billions'] = (df['val'] / 1e9).round(2)

    # Keep only the most recent n years
    df = df.tail(years).reset_index(drop=True)

    return df