"""Data loading utilities."""

from __future__ import annotations

import pandas as pd
import yfinance as yf


def _extract_close_frame(data: pd.DataFrame | pd.Series) -> pd.DataFrame:
    """Return a clean close-price dataframe from a yfinance download output."""
    if isinstance(data, pd.Series):
        return data.to_frame()

    if isinstance(data.columns, pd.MultiIndex):
        if "Close" in data.columns.get_level_values(0):
            close_prices = data["Close"].copy()
        else:
            close_prices = data.copy()
    else:
        close_prices = data.copy()

    if isinstance(close_prices, pd.Series):
        close_prices = close_prices.to_frame()

    close_prices = close_prices.dropna(how="all")
    if close_prices.empty:
        raise ValueError("Downloaded market data is empty after cleaning.")

    return close_prices


def download_close_prices(tickers: list[str], period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    """Download close prices for one or more tickers."""
    if not tickers:
        raise ValueError("At least one ticker must be provided.")

    data = yf.download(
        tickers=tickers,
        period=period,
        interval=interval,
        progress=False,
        auto_adjust=False,
        group_by="column",
        threads=True,
    )

    return _extract_close_frame(data)


def get_ticker_long_names(tickers: list[str]) -> dict[str, str]:
    """Return a mapping ticker -> company name."""
    names: dict[str, str] = {}
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            names[ticker] = info.get("longName", ticker)
        except Exception:
            names[ticker] = ticker
    return names


def get_company_summary(tickers: list[str]) -> pd.DataFrame:
    """Build a company summary table from Yahoo Finance metadata."""
    rows: list[dict[str, object]] = []

    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
        except Exception:
            info = {}

        trailing_pe = info.get("trailingPE")
        dividend_yield = info.get("dividendYield")
        market_cap = info.get("marketCap")
        revenue = info.get("totalRevenue")
        net_income = info.get("netIncomeToCommon")

        rows.append(
            {
                "Company Name": info.get("longName", ticker),
                "Ticker": ticker,
                "Industry": info.get("industry", "N/A"),
                "Market Cap (USD m)": round(market_cap / 1e6, 2) if market_cap else None,
                "Revenue (USD m)": round(revenue / 1e6, 2) if revenue else None,
                "Net Income (USD m)": round(net_income / 1e6, 2) if net_income else None,
                "Trailing P/E": round(trailing_pe, 2) if trailing_pe else None,
                "Dividend Yield (%)": round(dividend_yield * 100, 2) if dividend_yield else None,
            }
        )

    return pd.DataFrame(rows)
