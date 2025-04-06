# Aggressive MetaMask Trader

## Description
A high-speed terminal application for intelligent, math-driven Ethereum trading via MetaMask, leveraging real-time heuristics and market stats.

## Features
- Terminal interface
- Secure MetaMask wallet interaction
- Adaptive, math-driven trading logic
- Configurable parameters
- Logging for diagnostics and review

## Requirements
- Python 3.8+
- Dependencies:
  ```
  pip install web3 numpy scipy python-dotenv
  ```

## Usage
1. Configure `.env` with your private key and RPC URL
2. Adjust `config.ini` thresholds
3. Run:
  ```
  python main.py
  ```

## Security
Do not expose your `.env` file. Never hardcode sensitive data.

## Disclaimer
Use responsibly. Market conditions vary.
