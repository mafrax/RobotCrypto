from web3 import Web3
import json

class Token:
    def __init__(self, web3: Web3, address: str):
        self.web3 = web3
        self.address = Web3.toChecksumAddress(address)
        self.abi = json.loads(
            '[{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'
        )
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

    def get_symbol(self):
        try:
            return self.contract.functions.symbol().call()
        except Exception as e:
            print(f"Error getting symbol for token at {self.address}: {e}")
            return None

    def get_decimals(self):
        try:
            return self.contract.functions.decimals().call()
        except Exception as e:
            print(f"Error getting decimals for token at {self.address}: {e}")
            return None

    def get_total_supply(self):
        try:
            return self.contract.functions.totalSupply().call()
        except Exception as e:
            print(f"Error getting total supply for token at {self.address}: {e}")
            return None
