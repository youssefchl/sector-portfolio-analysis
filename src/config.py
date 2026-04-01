"""Project configuration."""

SECTOR_STOCKS = {
    "Technology": ["AAPL", "MSFT", "NVDA"],
    "Banking": ["JPM", "BAC", "GS"],
    "Healthcare": ["JNJ", "PFE", "MRK"],
    "Real Estate": ["AMT", "PLD", "CCI"],
    "Consumer Staples": ["PG", "KO", "PEP"],
    "Automotive": ["TSLA", "F", "GM"],
    "Energy": ["XOM", "CVX", "COP"],
}

SECTOR_BENCHMARKS = {
    "Technology": "^IXIC",
    "Banking": "^BKX",
    "Healthcare": "XLV",
    "Real Estate": "XLRE",
    "Consumer Staples": "XLP",
    "Automotive": "CARZ",
    "Energy": "XLE",
}

RISK_PROFILE_TARGET_VOL = {
    "Prudent": 0.15,
    "Balanced": 0.25,
    "Dynamic": 0.40,
}
