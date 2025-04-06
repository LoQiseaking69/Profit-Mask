import numpy as np
from scipy.stats import zscore
import configparser
import random
from logger import log_terminal

class AggressiveStrategy:
    def __init__(self, config_path='config.ini', price_feed_func=None):
        config = configparser.ConfigParser()
        read_files = config.read(config_path)
        if not read_files:
            raise FileNotFoundError(f"Config file '{config_path}' not found or unreadable.")

        try:
            trading_cfg = config['TRADING']
            self.token_address = trading_cfg.get('token_address')
            self.amount_eth = float(trading_cfg.get('amount_eth'))
            self.max_history = int(trading_cfg.get('price_history_length'))
            self.buy_slope = float(trading_cfg.get('buy_slope_threshold'))
            self.buy_zscore = float(trading_cfg.get('buy_zscore_threshold'))
            self.sell_slope = float(trading_cfg.get('sell_slope_threshold'))
            self.sell_zscore = float(trading_cfg.get('sell_zscore_threshold'))
        except Exception as e:
            raise RuntimeError(f"Invalid config values: {e}")

        if not self.token_address.startswith("0x") or len(self.token_address) != 42:
            raise ValueError("Invalid Ethereum token address format.")

        if not (0 < self.amount_eth < 100):
            raise ValueError("Configured amount_eth seems unsafe or unrealistic.")

        self.price_history = []
        self.price_feed_func = price_feed_func or self.default_price_feed

        # Analytics tracking
        self.last_decision = None
        self.last_price = None
        self.last_slope = None
        self.last_zscore = None
        self.last_stddev = None

    def default_price_feed(self):
        return round(random.uniform(0.4, 1.8), 5)  # Fallback/mock pricing

    def evaluate_market(self):
        try:
            price = self.price_feed_func()
        except Exception as e:
            log_terminal(f"ERROR – Price feed failure: {e}")
            return {"action": "hold", "reason": "price feed error"}

        self.price_history.append(price)
        if len(self.price_history) > self.max_history:
            self.price_history.pop(0)

        if len(self.price_history) < 6:
            log_terminal(f"HOLD – Insufficient data ({len(self.price_history)} samples)")
            return {"action": "hold", "reason": "not enough data"}

        prices = np.array(self.price_history)
        try:
            slope = np.mean(prices[-3:]) - np.mean(prices[:3])
            price_z = zscore(prices)[-1]
            std_dev = np.std(prices)
        except Exception as e:
            log_terminal(f"ERROR – Market math failure: {e}")
            return {"action": "hold", "reason": "math error"}

        self.last_decision = "hold"
        self.last_price = price
        self.last_slope = slope
        self.last_zscore = price_z
        self.last_stddev = std_dev

        log_terminal(
            f"Evaluating: price={price:.5f}, slope={slope:.5f}, z={price_z:.4f}, stddev={std_dev:.4f}"
        )

        if slope > self.buy_slope and price_z > self.buy_zscore and std_dev < 0.5:
            self.last_decision = "buy"
            return {
                "action": "buy",
                "token_address": self.token_address,
                "amount_eth": self.amount_eth,
                "reason": "buy conditions met"
            }
        elif slope < self.sell_slope and price_z < self.sell_zscore and std_dev > 0.4:
            self.last_decision = "sell"
            return {
                "action": "sell",
                "token_address": self.token_address,
                "amount_eth": self.amount_eth,
                "reason": "sell conditions met"
            }
        else:
            return {"action": "hold", "reason": "conditions not met"}
