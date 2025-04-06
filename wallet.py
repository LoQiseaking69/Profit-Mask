from web3 import Web3
from eth_account import Account
from decimal import Decimal
from logger import log_terminal

class Wallet:
    def __init__(self, private_key, rpc_url):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.w3.is_connected():
            raise ConnectionError(f"Unable to connect to RPC at {rpc_url}")
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.private_key = private_key
        log_terminal(f"Wallet initialized: {self.address}")

    def get_eth_balance(self):
        try:
            balance = self.w3.eth.get_balance(self.address)
            eth = self.w3.fromWei(balance, 'ether')
            log_terminal(f"Balance: {eth} ETH")
            return eth
        except Exception as e:
            log_terminal(f"ERROR – Balance fetch failed: {e}")
            return 0.0

    def get_nonce(self):
        try:
            return self.w3.eth.get_transaction_count(self.address)
        except Exception as e:
            log_terminal(f"ERROR – Nonce fetch failed: {e}")
            raise

    def get_gas_price(self):
        try:
            gas_price = self.w3.eth.generate_gas_price()
            if gas_price is None:
                gas_price = self.w3.eth.gas_price
            log_terminal(f"Gas price: {self.w3.fromWei(gas_price, 'gwei')} Gwei")
            return gas_price
        except Exception as e:
            log_terminal(f"ERROR – Gas price fetch failed: {e}")
            return self.w3.toWei(30, 'gwei')  # fallback default

    def sign_and_send(self, tx):
        try:
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            log_terminal(f"Transaction sent: {tx_hash.hex()}")
            return tx_hash.hex()
        except Exception as e:
            log_terminal(f"ERROR – TX signing/sending failed: {e}")
            raise

    def build_tx(self, to, value_eth, gas=21000, data=None):
        if value_eth is None or to is None:
            raise ValueError("Missing required fields: 'to' or 'value_eth'")
        try:
            value_wei = self.w3.toWei(Decimal(value_eth), 'ether')
            tx = {
                'to': to,
                'value': value_wei,
                'gas': gas,
                'gasPrice': self.get_gas_price(),
                'nonce': self.get_nonce(),
                'chainId': self.w3.eth.chain_id
            }
            if data:
                tx['data'] = data
            log_terminal(f"Built TX: to={to}, value={value_eth} ETH, gas={gas}")
            return tx
        except Exception as e:
            log_terminal(f"ERROR – TX build failed: {e}")
            raise
