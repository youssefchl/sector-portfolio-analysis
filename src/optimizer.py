import numpy as np
import pandas as pd
from scipy.optimize import minimize

from src.config import RISK_PROFILE_TARGET_VOL


def portfolio_performance(weights, mean_returns, cov_matrix):
    """
    Return expected return and volatility of a portfolio.
    """
    expected_return = float(weights @ mean_returns)
    volatility = float(np.sqrt(weights.T @ cov_matrix @ weights))
    return expected_return, volatility


def optimize_portfolio(returns: pd.DataFrame, risk_profile: str, amount: float):
    """
    Optimize long-only portfolio weights to match a target volatility.
    """
    if risk_profile not in RISK_PROFILE_TARGET_VOL:
        raise ValueError(f"Unknown risk profile: {risk_profile}")

    cov_matrix = returns.cov()
    mean_returns = returns.mean()
    n_assets = len(mean_returns)
    initial_weights = np.ones(n_assets) / n_assets
    target_vol = RISK_PROFILE_TARGET_VOL[risk_profile]

    def objective(weights):
        _, vol = portfolio_performance(weights, mean_returns, cov_matrix)
        return (vol - target_vol) ** 2

    constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
    bounds = [(0, 1)] * n_assets

    result = minimize(
        objective,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    if not result.success:
        raise ValueError(f"Optimization failed: {result.message}")

    weights = pd.Series(result.x, index=mean_returns.index, name="Weight")
    allocation_usd = pd.Series(result.x * amount, index=mean_returns.index, name="Allocation (USD)")

    return weights.round(4), allocation_usd.round(2)


def simulate_random_portfolios(
    returns: pd.DataFrame,
    n_portfolios: int = 5000,
    risk_free_rate: float = 0.0,
    random_state: int = 42,
):
    """
    Simulate random long-only portfolios and compute expected return,
    volatility and Sharpe ratio.
    """
    rng = np.random.default_rng(random_state)
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    n_assets = len(mean_returns)

    results = []

    for _ in range(n_portfolios):
        weights = rng.random(n_assets)
        weights = weights / weights.sum()

        exp_return = float(weights @ mean_returns)
        volatility = float(np.sqrt(weights.T @ cov_matrix @ weights))
        sharpe = (exp_return - risk_free_rate) / volatility if volatility > 0 else np.nan

        row = {
            "Return": exp_return,
            "Volatility": volatility,
            "Sharpe": sharpe,
        }

        for i, asset in enumerate(mean_returns.index):
            row[f"Weight_{asset}"] = weights[i]

        results.append(row)

    return pd.DataFrame(results)


def compute_efficient_frontier(
    returns: pd.DataFrame,
    points: int = 30,
):
    """
    Compute efficient frontier for long-only portfolios.
    """
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    n_assets = len(mean_returns)

    def portfolio_volatility(weights):
        return float(np.sqrt(weights.T @ cov_matrix @ weights))

    constraints_sum = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
    bounds = [(0, 1)] * n_assets

    min_ret = float(mean_returns.min())
    max_ret = float(mean_returns.max())
    target_returns = np.linspace(min_ret, max_ret, points)

    frontier = []

    for target_return in target_returns:
        constraints = [
            constraints_sum,
            {"type": "eq", "fun": lambda w, tr=target_return: float(w @ mean_returns) - tr},
        ]

        initial_weights = np.ones(n_assets) / n_assets

        result = minimize(
            portfolio_volatility,
            initial_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        if result.success:
            frontier.append(
                {
                    "Return": target_return,
                    "Volatility": portfolio_volatility(result.x),
                }
            )

    return pd.DataFrame(frontier)
