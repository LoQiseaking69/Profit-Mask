import os
import time
import signal
import threading
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

def main_loop():
    wallet = Wallet(os.getenv("PRIVATE_KEY"), os.getenv("RPC_URL"))
    strategy = AggressiveStrategy()
    engine = TradeEngine(wallet, strategy)

    while running:
        try:
            status = engine.execute_strategy()
            log_terminal(status)
        except Exception as e:
            log_terminal(f"ERROR: {e}")
        time.sleep(2)

if __name__ == "__main__":
    log_terminal(">>> Aggressive MetaMask Trader launched.")
    thread = threading.Thread(target=main_loop)
    thread.start()
    thread.join()
