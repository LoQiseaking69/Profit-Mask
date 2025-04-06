from logger import log_terminal
from utils import apply_gas_buffer

class TradeEngine:
    def __init__(self, wallet, strategy):
        self.wallet = wallet
        self.strategy = strategy

    def execute_strategy(self):
        decision = self.strategy.evaluate_market()
        action = decision.get("action")

        if action in ("buy", "sell"):
            tx = self.wallet.build_tx(
                to=decision["token_address"],
                value_eth=decision["amount_eth"],
                gas=apply_gas_buffer(decision.get("gas", 210000))
            )
            tx_hash = self.wallet.sign_and_send(tx)
            return f"{action.upper()} EXECUTED: TX = {tx_hash}"
        else:
            return "HOLD – Conditions not met."
