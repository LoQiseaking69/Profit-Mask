# Aggressive MetaMask Trader

## Description
A modular, high-speed Ethereum trading bot optimized for terminal execution. It uses real-time price data aligned with MetaMask-compatible sources and a math-driven strategy (slope, z-score, volatility) to make autonomous `buy`, `sell`, or `hold` decisions. It integrates secure Ethereum wallet interaction, database logging, and is backtest-ready.

## Features
- ✅ Secure Ethereum wallet control via Web3
- ✅ Adaptive strategy based on price slope, z-score, and volatility
- ✅ Real-time price fetching aligned with MetaMask RPC sources
- ✅ Periodic market evaluation and configurable gas buffering
- ✅ Configurable strategy thresholds via `config.ini`
- ✅ Persistent database logging (`SQLite`) for prices and trades
- ✅ Threaded execution with graceful shutdown on SIGINT/SIGTERM
- ✅ Supports live trading and simulated backtesting scaffolds
- ✅ Logs to terminal and file, customizable via `.env`

## Requirements
- Python 3.8+
- Dependencies:
  ```bash
  pip install web3 numpy scipy python-dotenv
  ```

## Configuration

### .env
```ini
PRIVATE_KEY=your_private_key_here
RPC_URL=https://mainnet.infura.io/v3/your_project_id
LOG_FILE=trading_log.txt
```

### config.ini
```ini
[TRADING]
token_address = 0x000000000000000000000000000000000000dead
amount_eth = 0.01
price_history_length = 30
buy_slope_threshold = 0.08
buy_zscore_threshold = 1.5
sell_slope_threshold = -0.08
sell_zscore_threshold = -1.5
```

## Usage
```bash
python main.py
```

## Database
- Creates `trading.db` on first run
- Tables:
  - `price_history` – every evaluated price
  - `trade_logs` – every trade action + metadata

## Logging
- Logs are saved to terminal and `trading_log.txt`
- Format: `[timestamp] [LEVEL] message`
- Log file path is configurable via `.env`

## Security
- **Never** commit your `.env` file
- Use testnet/private keys in development
- Use secure and rate-limited RPC URLs

## Disclaimer
This tool is experimental. Market conditions are volatile and unpredictable. Use with caution and at your own risk.
