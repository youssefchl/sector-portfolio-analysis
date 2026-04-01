# Sector-Based Portfolio Analysis and Optimization

## Overview
This project is a Python-based finance project designed to analyze a group of stocks within a selected market sector and produce a simple optimized allocation based on an investor risk profile.

It uses historical market data from Yahoo Finance to compute:
- price evolution
- base-100 normalized performance
- return correlations
- stock betas versus a sector benchmark
- a long-only portfolio allocation inspired by Markowitz-style optimization

## Why this project matters
This repository is built to showcase practical skills relevant for economics and finance applications:
- Python for financial analysis
- market data handling
- risk/return reasoning
- portfolio construction
- project organization for GitHub

## Project structure
```text
sector-portfolio-analysis/
├── notebooks/
│   └── sector_portfolio_analysis.ipynb
├── outputs/
├── src/
│   ├── __init__.py
│   ├── analytics.py
│   ├── config.py
│   ├── data_loader.py
│   ├── main.py
│   ├── optimizer.py
│   └── reporting.py
├── tests/
│   ├── __init__.py
│   ├── test_analytics.py
│   └── test_optimizer.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Features
- Sector-based stock selection
- Historical price download with `yfinance`
- Daily and monthly return logic
- Base 100 normalization
- Correlation matrix computation
- Beta estimation versus a benchmark
- Risk-profile-based portfolio optimization
- Clean modular Python structure
- Basic unit tests with `pytest`

## Available sectors
- Technology
- Banking
- Healthcare
- Real Estate
- Consumer Staples
- Automotive
- Energy

## Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/sector-portfolio-analysis.git
cd sector-portfolio-analysis
pip install -r requirements.txt
```

## Usage
Run the main script:

```bash
python -m src.main
```

Or open the notebook:

```bash
jupyter notebook notebooks/sector_portfolio_analysis.ipynb
```

## Tests
Run:

```bash
pytest
```

## Main files
- `src/data_loader.py`: downloads market data and company metadata
- `src/analytics.py`: computes returns, base 100, correlation and beta
- `src/optimizer.py`: builds the optimized allocation
- `src/main.py`: runs the full pipeline
- `notebooks/sector_portfolio_analysis.ipynb`: presentation notebook version

## Academic and CV positioning
A clean way to describe this project on a CV is:

**Sector-Based Portfolio Analysis and Optimization (Python)**  
Built a Python project using Yahoo Finance data to analyze sector stocks, compute risk indicators, and generate an optimized portfolio allocation based on investor profile.

## Possible future improvements
- Sharpe ratio maximization
- efficient frontier visualization
- backtesting
- reporting dashboard
- richer benchmark selection
