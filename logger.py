import datetime
import threading
import os

LOG_FILE = os.getenv("LOG_FILE", "trading_log.txt")
_log_lock = threading.Lock()

def log_terminal(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = f"[{timestamp}] [{level}] {message}"
    print(output)

    try:
        with _log_lock:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(output + "\n")
    except Exception as e:
        print(f"[{timestamp}] [ERROR] Failed to write to log file: {e}")
