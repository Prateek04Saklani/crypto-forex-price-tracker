# Crypto & Forex Price Tracker

A command-line tool to track real-time cryptocurrency and forex market data, with volatility analysis and price alerts.

## Features

- **Price Tracker** (`price_tracker.py`): Fetch live prices for multiple cryptocurrencies and forex pairs in a formatted table view.
- **Volatility Analyzer** (`volatile_analysis.py`): Deep-dive analysis for a single asset including volatility metrics, market sentiment (Fear & Greed Index), support/resistance levels, and email price alerts.

## Setup

```bash
pip install requests python-dotenv
```

For email alerts, create a `.env` file:

```
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password
```

## Usage

### Price Tracker

```bash
python price_tracker.py
```

Enter comma-separated crypto IDs (e.g. `bitcoin,ethereum`) and forex pairs (e.g. `USD/EUR,GBP/USD`), or press Enter to use defaults.

### Volatility Analyzer

```bash
python volatile_analysis.py
```

Choose to analyze a crypto asset or forex pair. For crypto, you can optionally set a price alert that monitors the asset and sends an email notification when the target is reached.

## APIs Used

- [CoinGecko](https://www.coingecko.com/en/api) — Cryptocurrency market data
- [ExchangeRate-API](https://www.exchangerate-api.com/) — Forex exchange rates
- [Alternative.me](https://alternative.me/crypto/fear-and-greed-index/) — Fear & Greed Index
