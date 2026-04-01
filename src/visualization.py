import matplotlib.pyplot as plt


def plot_efficient_frontier(portfolios, frontier, output_path="outputs/efficient_frontier.png"):
    """
    Plot random portfolios and efficient frontier, then save the figure.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(
        portfolios["Volatility"],
        portfolios["Return"],
        c=portfolios["Sharpe"],
        alpha=0.5,
    )
    plt.plot(
        frontier["Volatility"],
        frontier["Return"],
        linewidth=2,
    )
    plt.xlabel("Volatility")
    plt.ylabel("Expected Return")
    plt.title("Efficient Frontier")
    plt.colorbar(label="Sharpe Ratio")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
