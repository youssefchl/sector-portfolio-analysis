"""Main entry point for the project."""

from __future__ import annotations

from pathlib import Path

from src.analytics import compute_base100, compute_betas, compute_correlation_matrix, compute_daily_log_returns
from src.config import SECTOR_BENCHMARKS, SECTOR_STOCKS
from src.data_loader import download_close_prices, get_company_summary
from src.optimizer import optimize_portfolio
from src.reporting import save_base100_chart, save_price_chart
from src.optimizer import simulate_random_portfolios, compute_efficient_frontier
from src.visualization import plot_efficient_frontier

def run_sector_analysis(
    sector: str = "Technology",
    risk_profile: str = "Balanced",
    amount: float = 10_000.0,
):
    """Run the full sector analysis pipeline."""
    if sector not in SECTOR_STOCKS:
        raise ValueError(f"Unknown sector: {sector}")

    tickers = SECTOR_STOCKS[sector]
    benchmark = SECTOR_BENCHMARKS[sector]

    asset_prices = download_close_prices(tickers)
    benchmark_prices = download_close_prices([benchmark])

    asset_returns = compute_daily_log_returns(asset_prices)
    benchmark_returns = compute_daily_log_returns(benchmark_prices).iloc[:, 0]

    base100 = compute_base100(asset_prices)
    correlation = compute_correlation_matrix(asset_returns)
    betas = compute_betas(asset_returns, benchmark_returns)
    company_summary = get_company_summary(tickers)
    weights, allocation = optimize_portfolio(asset_returns, risk_profile, amount)
    portfolios = simulate_random_portfolios(asset_returns)
    frontier = compute_efficient_frontier(asset_returns)
    plot_efficient_frontier(portfolios, frontier)
    output_dir = Path("outputs")
    save_price_chart(asset_prices, output_dir / "prices.png", f"{sector} sector stock prices")
    save_base100_chart(base100, output_dir / "base100.png", f"{sector} sector performance (base 100)")

    return {
        "prices": asset_prices,
        "returns": asset_returns,
        "base100": base100,
        "correlation": correlation,
        "betas": betas,
        "company_summary": company_summary,
        "weights": weights,
        "allocation": allocation,
    }


if __name__ == "__main__":
    results = run_sector_analysis()
    print("=== Optimized Portfolio Weights ===")
    print(results["weights"].to_string())
    print("\n=== Allocation (USD) ===")
    print(results["allocation"].to_string())
