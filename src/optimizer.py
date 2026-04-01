"""Portfolio optimization logic."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from src.config import RISK_PROFILE_TARGET_VOL


def portfolio_performance(weights: np.ndarray, mean_returns: pd.Series, cov_matrix: pd.DataFrame) -> tuple[float, float]:
    """Return expected portfolio return and volatility."""
    expected_return = float(weights @ mean_returns.values)
    volatility = float(np.sqrt(weights.T @ cov_matrix.values @ weights))
    return expected_return, volatility


def optimize_portfolio(returns: pd.DataFrame, risk_profile: str, amount: float) -> tuple[pd.Series, pd.Series]:
    """Optimize a long-only portfolio with a target volatility objective."""
    if returns.empty:
        raise ValueError("Returns dataframe is empty.")
    if amount <= 0:
        raise ValueError("Investment amount must be strictly positive.")
    if risk_profile not in RISK_PROFILE_TARGET_VOL:
        raise ValueError(f"Unknown risk profile: {risk_profile}")

    cov_matrix = returns.cov()
    mean_returns = returns.mean()
    n_assets = len(mean_returns)
    initial_weights = np.repeat(1 / n_assets, n_assets)
    target_vol = RISK_PROFILE_TARGET_VOL[risk_profile]

    def objective(weights: np.ndarray) -> float:
        _, vol = portfolio_performance(weights, mean_returns, cov_matrix)
        return (vol - target_vol) ** 2

    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
    bounds = [(0.0, 1.0)] * n_assets

    result = minimize(
        objective,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    if not result.success:
        raise ValueError(f"Optimization failed: {result.message}")

    weights = pd.Series(result.x, index=mean_returns.index, name="Weight").round(6)
    allocations = pd.Series(result.x * amount, index=mean_returns.index, name="Allocation (USD)").round(2)

    return weights, allocations
