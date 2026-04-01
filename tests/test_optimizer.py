import pandas as pd
import pytest

from src.optimizer import optimize_portfolio


def sample_returns():
    return pd.DataFrame(
        {
            "AAPL": [0.01, 0.02, -0.01, 0.015, 0.01],
            "MSFT": [0.008, 0.018, -0.005, 0.011, 0.007],
            "NVDA": [0.02, 0.03, -0.02, 0.025, 0.021],
        }
    )


def test_optimize_portfolio_weights_sum_to_one():
    weights, allocation = optimize_portfolio(sample_returns(), risk_profile="Balanced", amount=1000)

    assert abs(weights.sum() - 1) < 1e-5
    assert len(weights) == 3
    assert len(allocation) == 3


def test_optimize_portfolio_has_no_negative_weights():
    weights, _ = optimize_portfolio(sample_returns(), risk_profile="Prudent", amount=1000)

    assert (weights >= 0).all()
    assert (weights <= 1).all()


def test_optimize_portfolio_rejects_invalid_amount():
    with pytest.raises(ValueError):
        optimize_portfolio(sample_returns(), risk_profile="Balanced", amount=0)
