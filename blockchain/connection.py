from web3 import Web3

class BlockchainConnection:
    def __init__(self):
        self.infura_url = 'https://api.avax.network/ext/bc/C/rpc'

    def connect(self):
        return Web3(Web3.HTTPProvider(self.infura_url))
