from web3 import Web3
from eth_account import Account
from decimal import Decimal

class Wallet:
    def __init__(self, private_key, rpc_url):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.private_key = private_key

    def get_eth_balance(self):
        balance = self.w3.eth.get_balance(self.address)
        return self.w3.fromWei(balance, 'ether')

    def get_nonce(self):
        return self.w3.eth.get_transaction_count(self.address)

    def get_gas_price(self):
        return self.w3.eth.generate_gas_price() or self.w3.eth.gas_price

    def sign_and_send(self, tx):
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()

    def build_tx(self, to, value_eth, gas=21000):
        value_wei = self.w3.toWei(Decimal(value_eth), 'ether')
        return {
            'to': to,
            'value': value_wei,
            'gas': gas,
            'gasPrice': self.get_gas_price(),
            'nonce': self.get_nonce(),
            'chainId': self.w3.eth.chain_id
        }
