import numpy as np
from scipy.stats import zscore
import configparser
import random

class AggressiveStrategy:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.token_address = config.get('TRADING', 'token_address')
        self.amount_eth = float(config.get('TRADING', 'amount_eth'))
        self.max_history = int(config.get('TRADING', 'price_history_length'))
        self.buy_slope = float(config.get('TRADING', 'buy_slope_threshold'))
        self.buy_zscore = float(config.get('TRADING', 'buy_zscore_threshold'))
        self.sell_slope = float(config.get('TRADING', 'sell_slope_threshold'))
        self.sell_zscore = float(config.get('TRADING', 'sell_zscore_threshold'))

        self.price_history = []

    def fetch_latest_price(self):
        return round(random.uniform(0.4, 1.8), 5)

    def evaluate_market(self):
        price = self.fetch_latest_price()
        self.price_history.append(price)
        if len(self.price_history) > self.max_history:
            self.price_history.pop(0)

        if len(self.price_history) < 6:
            return {"action": "hold"}

        prices = np.array(self.price_history)
        slope = np.mean(prices[-3:]) - np.mean(prices[:3])
        price_z = zscore(prices)[-1]
        std_dev = np.std(prices)

        if slope > self.buy_slope and price_z > self.buy_zscore and std_dev < 0.5:
            return {"action": "buy", "token_address": self.token_address, "amount_eth": self.amount_eth}
        elif slope < self.sell_slope and price_z < self.sell_zscore and std_dev > 0.4:
            return {"action": "sell", "token_address": self.token_address, "amount_eth": self.amount_eth}
        else:
            return {"action": "hold"}
