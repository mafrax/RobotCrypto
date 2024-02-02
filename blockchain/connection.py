import os
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

load_dotenv()


class BlockchainConnection:
    def __init__(self):
        self.infura_url = 'https://api.avax.network/ext/bc/C/rpc'
        # Load private key from environment variable
        self.private_key = os.getenv('PRIVATE_KEY')
        self.web3 = None
        self.account = None

    def connect(self):
        self.web3 = Web3(HTTPProvider(self.infura_url))
        # Insert middleware to support the PoA consensus used by some networks like AVAX C-Chain
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        print(os.getenv('PRIVATE_KEY'))  # This should print your private key if loaded correctly

        if self.web3.is_connected():
            print("Connected to the Blockchain")
            if self.private_key:
                self.account = self.web3.eth.account.from_key(self.private_key)
                print(f"Account {self.account.address} loaded")
            else:
                print("No private key provided, read-only mode")
        else:
            print("Failed to connect to the Blockchain")

        return self.web3
