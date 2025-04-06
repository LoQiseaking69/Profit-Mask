from logger import log_terminal
from utils import apply_gas_buffer

class TradeEngine:
    def __init__(self, wallet, strategy):
        self.wallet = wallet
        self.strategy = strategy

    def execute_strategy(self):
        try:
            decision = self.strategy.evaluate_market()
            action = decision.get("action")

            if action in ("buy", "sell"):
                token_address = decision.get("token_address")
                amount_eth = decision.get("amount_eth")

                if not token_address or amount_eth is None:
                    log_terminal(f"Invalid decision data: {decision}")
                    return "ERROR – Incomplete trade decision."

                gas_limit = apply_gas_buffer(decision.get("gas", 210000))
                tx = self.wallet.build_tx(
                    to=token_address,
                    value_eth=amount_eth,
                    gas=gas_limit
                )
                tx_hash = self.wallet.sign_and_send(tx)
                msg = f"{action.upper()} EXECUTED: TX = {tx_hash}"
                log_terminal(msg)
                return msg

            log_terminal("Strategy decision: HOLD")
            return "HOLD – Conditions not met."

        except Exception as e:
            err_msg = f"Trade execution failed: {str(e)}"
            log_terminal(err_msg)
            return f"ERROR – {err_msg}"
