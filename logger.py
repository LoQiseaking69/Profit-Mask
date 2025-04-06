import datetime

LOG_FILE = "trading_log.txt"

def log_terminal(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = f"[{timestamp}] {message}"
    print(output)
    with open(LOG_FILE, "a") as f:
        f.write(output + "\n")
