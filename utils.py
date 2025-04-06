from logger import log_terminal

def estimate_slippage(expected_price, actual_price):
    if expected_price <= 0:
        log_terminal(f"WARNING – Invalid expected price: {expected_price}")
        return 0.0
    slippage = ((actual_price - expected_price) / expected_price) * 100
    log_terminal(f"Slippage calculated: {slippage:.4f}% (expected: {expected_price}, actual: {actual_price})")
    return round(slippage, 4)

def apply_gas_buffer(base_gas, buffer_percent=15):
    if base_gas <= 0:
        log_terminal(f"WARNING – Invalid base gas value: {base_gas}")
        return 21000  # default safe fallback

    buffer_percent = max(0, min(buffer_percent, 100))  # clamp to [0, 100]
    adjusted_gas = int(base_gas * (1 + buffer_percent / 100))
    log_terminal(f"Gas adjusted from {base_gas} to {adjusted_gas} (+{buffer_percent}%)")
    return adjusted_gas
