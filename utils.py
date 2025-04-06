def estimate_slippage(expected_price, actual_price):
    if expected_price == 0:
        return 0.0
    return round(((actual_price - expected_price) / expected_price) * 100, 4)

def apply_gas_buffer(base_gas, buffer_percent=15):
    return int(base_gas * (1 + buffer_percent / 100))
