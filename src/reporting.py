"""Reporting and plotting helpers."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_price_chart(prices: pd.DataFrame, output_path: str | Path, title: str) -> Path:
    """Save a line chart of price series."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(11, 5))
    for col in prices.columns:
        plt.plot(prices.index, prices[col], label=col, linewidth=2)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path


def save_base100_chart(base100: pd.DataFrame, output_path: str | Path, title: str) -> Path:
    """Save a base-100 performance chart."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(11, 5))
    for col in base100.columns:
        plt.plot(base100.index, base100[col], label=col, linewidth=2)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Base 100")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path
