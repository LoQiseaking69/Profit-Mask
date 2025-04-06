
import os
import time
import signal
import threading
import sqlite3
from wallet import Wallet
from trade_engine import TradeEngine
from strategy import AggressiveStrategy
from logger import log_terminal
from dotenv import load_dotenv

load_dotenv()
running = True

def signal_handler(sig, frame):
    global running
    running = False
    log_terminal("Shutting down gracefully...")

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def init_db():
    conn = sqlite3.connect("trading.db")
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trade_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                price REAL NOT NULL,
                slope REAL,
                zscore REAL,
                stddev REAL,
                reason TEXT,
                tx_hash TEXT
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                price REAL NOT NULL
            );
        """)
    return conn

def save_trade(conn, action, price, slope, zscore, stddev, reason, tx_hash=None):
    with conn:
        conn.execute("""
            INSERT INTO trade_logs (timestamp, action, price, slope, zscore, stddev, reason, tx_hash)
            VALUES (datetime('now'), ?, ?, ?, ?, ?, ?, ?)
        """, (action, price, slope, zscore, stddev, reason, tx_hash))

def save_price(conn, price):
    with conn:
        conn.execute("""
            INSERT INTO price_history (timestamp, price)
            VALUES (datetime('now'), ?)
        """, (price,))

def main_loop():
    conn = init_db()
    wallet = Wallet(os.getenv("PRIVATE_KEY"), os.getenv("RPC_URL"))
    strategy = AggressiveStrategy()
    engine = TradeEngine(wallet, strategy)

    while running:
        try:
            decision = strategy.evaluate_market()
            action = decision.get("action")
            reason = decision.get("reason", "N/A")
            price = strategy.last_price or 0.0
            slope = strategy.last_slope
            zscore = strategy.last_zscore
            stddev = strategy.last_stddev
            save_price(conn, price)

            if action in ("buy", "sell"):
                result = engine.execute_strategy()
                tx_hash = result.split("TX = ")[-1] if "TX =" in result else None
                save_trade(conn, action, price, slope, zscore, stddev, reason, tx_hash)
                log_terminal(result)
            else:
                save_trade(conn, action, price, slope, zscore, stddev, reason)
                log_terminal(f"HOLD – {reason}")
        except Exception as e:
            log_terminal(f"ERROR: {e}")
        time.sleep(2)

if __name__ == "__main__":
    log_terminal(">>> Aggressive MetaMask Trader launched.")
    thread = threading.Thread(target=main_loop)
    thread.start()
    thread.join()
