# ratios.py
import pandas as pd

def calculate_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates key financial ratios from the master DataFrame.
    
    Ratios are grouped into four categories:
    - Profitability: how well the company generates profit
    - Efficiency: how well it uses its assets
    - Leverage: how much debt it carries
    - Cash Flow: quality of earnings
    """
    ratios = pd.DataFrame()
    ratios['fiscal_year'] = df['fiscal_year']

    # ── Profitability ──────────────────────────────────────────
    # Gross Margin: how much is left after cost of goods
    # A rising gross margin = pricing power or cost discipline
    ratios['gross_margin_%'] = (
        df['gross_profit'] / df['revenue'] * 100
    ).round(1)

    # Operating Margin: profitability from core business
    # Strips out interest and tax — pure operational efficiency
    ratios['operating_margin_%'] = (
        df['operating_income'] / df['revenue'] * 100
    ).round(1)

    # Net Margin: bottom line after everything
    ratios['net_margin_%'] = (
        df['net_income'] / df['revenue'] * 100
    ).round(1)

    # Return on Equity: profit generated per dollar of equity
    # Warren Buffett's favourite — consistently high ROE = moat
    ratios['roe_%'] = (
        df['net_income'] / df['equity'] * 100
    ).round(1)

    # Return on Assets: profit generated per dollar of assets
    ratios['roa_%'] = (
        df['net_income'] / df['total_assets'] * 100
    ).round(1)

    # ── Efficiency ─────────────────────────────────────────────
    # Revenue Growth YoY: is the business growing?
    ratios['revenue_growth_%'] = (
        df['revenue'].pct_change() * 100
    ).round(1)

    # Net Income Growth YoY
    ratios['net_income_growth_%'] = (
        df['net_income'].pct_change() * 100
    ).round(1)

    # ── Leverage ───────────────────────────────────────────────
    # Debt to Equity: how leveraged is the balance sheet?
    # High D/E isn't always bad — Apple deliberately levers up
    # for buybacks, so context matters
    ratios['debt_to_equity'] = (
        df['long_term_debt'] / df['equity']
    ).round(2)

    # Debt to Assets: what proportion of assets are debt-funded
    ratios['debt_to_assets'] = (
        df['long_term_debt'] / df['total_assets']
    ).round(2)

    # ── Cash Flow Quality ──────────────────────────────────────
    # FCF: operating cash flow minus capex
    # The real cash the business generates after maintenance
    ratios['fcf'] = df['operating_cashflow'] - df['capex']

    # FCF Margin: FCF as a % of revenue
    # High FCF margin = capital light, high quality business
    ratios['fcf_margin_%'] = (
        ratios['fcf'] / df['revenue'] * 100
    ).round(1)

    # Cash Conversion: how much net income becomes FCF
    # > 100% means the business generates more cash than
    # accounting profit suggests — a quality signal
    ratios['cash_conversion_%'] = (
        ratios['fcf'] / df['net_income'] * 100
    ).round(1)

    return ratios