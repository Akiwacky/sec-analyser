import plotly.graph_objects as go
import pandas as pd

# ── Colour palette ─────────────────────────────────────────────
BACKGROUND = "#0d1b2a"
TEXT = "#e0e1dd"
GRID = "#1e2d3d"
BLUE = "#415a77"
LIGHT_BLUE = "#778da9"
ACCENT = "#e0e1dd"
BACKGROUND = "#0d1b2a"
TEXT = "#e0e1dd"


# Distinct chart colours — readable on dark background
COLORS = {
    "blue":    "#4895ef",
    "teal":    "#4cc9f0",
    "green":   "#80ffdb",
    "yellow":  "#ffd60a",
    "orange":  "#f77f00",
    "red":     "#e63946",
    "purple":  "#b5179e",
    "grey":    "#778da9",
}


def base_layout(title: str) -> dict:
    """
    Shared layout settings applied to all charts.
    yaxis is intentionally excluded — each chart defines its own.
    """
    return dict(
        title=dict(
            text=title,
            font=dict(size=20, color=TEXT),
            x=0.05
        ),
        plot_bgcolor=BACKGROUND,
        paper_bgcolor=BACKGROUND,
        font=dict(color=TEXT, family="Arial"),
        xaxis=dict(
            showgrid=False,
            color=TEXT,
            tickfont=dict(size=11),
            tickmode='linear'
        ),
        legend=dict(
            bgcolor=BACKGROUND,
            bordercolor=LIGHT_BLUE,
            borderwidth=1
        ),
        margin=dict(l=60, r=40, t=60, b=60)
    )


def plot_margins(ratios: pd.DataFrame, ticker: str):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ratios['fiscal_year'],
        y=ratios['gross_margin_%'],
        name='Gross Margin',
        mode='lines+markers',
        line=dict(color=COLORS['blue'], width=2.5),
        marker=dict(size=6)
    ))

    fig.add_trace(go.Scatter(
        x=ratios['fiscal_year'],
        y=ratios['operating_margin_%'],
        name='Operating Margin',
        mode='lines+markers',
        line=dict(color=COLORS['teal'], width=2.5),
        marker=dict(size=6)
    ))

    fig.add_trace(go.Scatter(
        x=ratios['fiscal_year'],
        y=ratios['net_margin_%'],
        name='Net Margin',
        mode='lines+markers',
        line=dict(color=COLORS['green'], width=2.5),
        marker=dict(size=6)
    ))

    fig.update_layout(
        **base_layout(f"{ticker} — Profit Margins (%)"),
        yaxis=dict(
            ticksuffix='%',
            showgrid=True,
            gridcolor=GRID,
            color=TEXT,
            tickfont=dict(size=11)
        )
    )

    return fig


def plot_returns(ratios: pd.DataFrame, ticker: str):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ratios['fiscal_year'],
        y=ratios['roe_%'],
        name='ROE',
        mode='lines+markers',
        line=dict(color=COLORS['yellow'], width=2.5),
        marker=dict(size=6)
    ))

    fig.add_trace(go.Scatter(
        x=ratios['fiscal_year'],
        y=ratios['roa_%'],
        name='ROA',
        mode='lines+markers',
        line=dict(color=COLORS['orange'], width=2.5),
        marker=dict(size=6)
    ))

    fig.update_layout(
        **base_layout(f"{ticker} — Return on Equity vs Assets (%)"),
        yaxis=dict(
            ticksuffix='%',
            showgrid=True,
            gridcolor=GRID,
            color=TEXT,
            tickfont=dict(size=11)
        )
    )

    return fig


def plot_growth(ratios: pd.DataFrame, ticker: str):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=ratios['fiscal_year'],
        y=ratios['revenue_growth_%'],
        name='Revenue Growth',
        marker_color=COLORS['blue'],
        opacity=0.85
    ))

    fig.add_trace(go.Bar(
        x=ratios['fiscal_year'],
        y=ratios['net_income_growth_%'],
        name='Net Income Growth',
        marker_color=COLORS['green'],
        opacity=0.85
    ))

    fig.add_hline(
        y=0,
        line_color=TEXT,
        line_width=1,
        opacity=0.4
    )

    fig.update_layout(
        **base_layout(f"{ticker} — Revenue & Net Income Growth (% YoY)"),
        barmode='group',
        yaxis=dict(
            ticksuffix='%',
            showgrid=True,
            gridcolor=GRID,
            color=TEXT,
            tickfont=dict(size=11)
        )
    )

    return fig


def plot_cashflow(ratios: pd.DataFrame, ticker: str):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=ratios['fiscal_year'],
        y=ratios['fcf_margin_%'],
        name='FCF Margin',
        marker_color=COLORS['teal'],
        opacity=0.85,
        yaxis='y1'
    ))

    fig.add_trace(go.Scatter(
        x=ratios['fiscal_year'],
        y=ratios['cash_conversion_%'],
        name='Cash Conversion',
        mode='lines+markers',
        line=dict(color=COLORS['yellow'], width=2.5),
        marker=dict(size=6),
        yaxis='y2'
    ))

    # Reference line at 100% cash conversion
    fig.add_hline(
        y=100,
        line_color=TEXT,
        line_width=1,
        line_dash='dash',
        opacity=0.4,
        annotation_text="100% conversion",
        annotation_position="top right",
        annotation_font_color=TEXT
    )

    fig.update_layout(
        **base_layout(f"{ticker} — Cash Flow Quality"),
        yaxis=dict(
            title='FCF Margin %',
            ticksuffix='%',
            showgrid=True,
            gridcolor=GRID,
            color=TEXT,
            tickfont=dict(size=11)
        ),
        yaxis2=dict(
            title='Cash Conversion %',
            ticksuffix='%',
            overlaying='y',
            side='right',
            showgrid=False,
            color=COLORS['yellow'],
            tickfont=dict(size=11)
        )
    )

    return fig


def plot_leverage(ratios: pd.DataFrame, ticker: str):
    leverage = ratios.dropna(subset=['debt_to_equity', 'debt_to_assets'])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=leverage['fiscal_year'],
        y=leverage['debt_to_equity'],
        name='Debt / Equity',
        mode='lines+markers',
        line=dict(color=COLORS['red'], width=2.5),
        marker=dict(size=6)
    ))

    fig.add_trace(go.Scatter(
        x=leverage['fiscal_year'],
        y=leverage['debt_to_assets'],
        name='Debt / Assets',
        mode='lines+markers',
        line=dict(color=COLORS['orange'], width=2.5),
        marker=dict(size=6)
    ))

    fig.update_layout(
        **base_layout(f"{ticker} — Leverage Ratios"),
        yaxis=dict(
            showgrid=True,
            gridcolor=GRID,
            color=TEXT,
            tickfont=dict(size=11)
        )
    )

    return fig

def show_all(ratios: pd.DataFrame, ticker: str):
    """
    Renders all five charts in sequence.
    Each opens as an interactive chart in the browser.
    """
    charts = [
        plot_margins(ratios, ticker),
        plot_returns(ratios, ticker),
        plot_growth(ratios, ticker),
        plot_cashflow(ratios, ticker),
        plot_leverage(ratios, ticker),
    ]

    for chart in charts:
        chart.show()