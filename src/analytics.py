"""Analytics functions for portfolio analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_daily_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute daily log returns from price series."""
    if prices.empty:
        raise ValueError("Price dataframe is empty.")
    return np.log(prices / prices.shift(1)).dropna(how="all")


def compute_monthly_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute monthly log returns from month-end prices."""
    if prices.empty:
        raise ValueError("Price dataframe is empty.")
    monthly_prices = prices.resample("ME").last()
    return np.log(monthly_prices / monthly_prices.shift(1)).dropna(how="all")


def compute_base100(prices: pd.DataFrame) -> pd.DataFrame:
    """Normalize prices to base 100."""
    if prices.empty:
        raise ValueError("Price dataframe is empty.")
    first_row = prices.iloc[0]
    if (first_row == 0).any():
        raise ValueError("Base 100 cannot be computed with zero starting prices.")
    return (prices / first_row) * 100


def compute_correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    """Compute correlation matrix."""
    if returns.empty:
        raise ValueError("Returns dataframe is empty.")
    return returns.corr()


def compute_beta(stock_returns: pd.Series, benchmark_returns: pd.Series) -> float:
    """Compute beta of one asset relative to a benchmark."""
    aligned = pd.concat([stock_returns, benchmark_returns], axis=1).dropna()
    aligned.columns = ["stock", "benchmark"]

    if len(aligned) < 2:
        raise ValueError("At least two aligned return observations are required to compute beta.")

    benchmark_var = aligned["benchmark"].var(ddof=0)
    if benchmark_var == 0:
        raise ValueError("Benchmark variance is zero; beta cannot be computed.")

    covariance = np.cov(aligned["stock"], aligned["benchmark"], ddof=0)[0, 1]
    return float(covariance / benchmark_var)


def compute_betas(asset_returns: pd.DataFrame, benchmark_returns: pd.Series) -> pd.Series:
    """Compute beta for each asset in a return dataframe."""
    if asset_returns.empty:
        raise ValueError("Asset returns dataframe is empty.")

    betas = {col: compute_beta(asset_returns[col], benchmark_returns) for col in asset_returns.columns}
    return pd.Series(betas, name="Beta")
