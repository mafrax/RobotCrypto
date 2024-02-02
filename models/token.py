from web3 import Web3
import json
import os

class Token:
    def __init__(self, web3: Web3, address: str):
        self.web3 = web3
        self.address = address
        # Get the current working directory
        current_directory = os.getcwd()

        # Specify the path to the ABI file
        abi_file_path = os.path.join(current_directory, './models/token_abi.json')

        # Check if the ABI file exists
        if os.path.exists(abi_file_path):
            # Load the ERC-20 ABI from the JSON file
            with open(abi_file_path, 'r') as abi_file:
                self.abi = json.load(abi_file)
        else:
            print(f"ABI file 'token_abi.json' not found in the current directory: {abi_file_path}")
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

    def get_balance(self, address):
        """Get the balance of this token for a specific address."""
        return self.contract.functions.balanceOf(address).call()

    def format_liquidity(self, liquidity):
        # Convert from wei to Ether (or the base unit to the token standard unit)
        decimals = self.get_decimals()
        liquidity_in_token = liquidity
                              # / 1e18)  # Adjust this divisor based on the token's decimals

        if liquidity_in_token >= 1e9:
            return f"{liquidity_in_token / 1e9:.2f}B"
        elif liquidity_in_token >= 1e6:
            return f"{liquidity_in_token / 1e6:.2f}M"
        elif liquidity_in_token >= 1e3:
            return f"{liquidity_in_token / 1e3:.2f}K"
        else:
            return f"{liquidity_in_token:.2f}"
