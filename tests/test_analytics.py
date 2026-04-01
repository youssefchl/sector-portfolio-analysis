import numpy as np
import pandas as pd
import pytest

from src.analytics import compute_base100, compute_beta, compute_correlation_matrix, compute_daily_log_returns


def test_compute_base100_starts_at_100():
    prices = pd.DataFrame({"AAPL": [100, 110, 120], "MSFT": [200, 210, 220]})
    base100 = compute_base100(prices)

    assert base100.iloc[0, 0] == 100
    assert base100.iloc[0, 1] == 100


def test_compute_daily_log_returns_shape():
    prices = pd.DataFrame({"AAPL": [100, 110, 121], "MSFT": [200, 220, 242]})
    returns = compute_daily_log_returns(prices)

    assert returns.shape == (2, 2)
    assert list(returns.columns) == ["AAPL", "MSFT"]


def test_compute_correlation_matrix_is_square():
    returns = pd.DataFrame({"AAPL": [0.01, 0.02, -0.01], "MSFT": [0.02, 0.01, -0.02]})
    corr = compute_correlation_matrix(returns)

    assert corr.shape == (2, 2)


def test_compute_beta_returns_float():
    stock = pd.Series([0.01, 0.02, 0.015, -0.005])
    benchmark = pd.Series([0.008, 0.018, 0.012, -0.004])

    beta = compute_beta(stock, benchmark)
    assert isinstance(beta, float)
    assert not np.isnan(beta)


def test_compute_beta_raises_when_benchmark_variance_zero():
    stock = pd.Series([0.01, 0.02, 0.03])
    benchmark = pd.Series([0.01, 0.01, 0.01])

    with pytest.raises(ValueError):
        compute_beta(stock, benchmark)
