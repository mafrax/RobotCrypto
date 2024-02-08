import os
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.publickey import PublicKey
from base58 import b58encode, b58decode
from dotenv import load_dotenv

load_dotenv()


class SolanaBlockchainConnection:
    def __init__(self):
        # Use a public Solana RPC endpoint or configure your own
        self.rpc_url = 'https://api.mainnet-beta.solana.com'
        self.client = None
        self.wallet = None
        self.public_key = None

    def connect(self):
        self.client = Client(self.rpc_url)

        # Load private key from environment variable
        private_key_str = os.getenv('SOLANA_PRIVATE_KEY')
        if private_key_str:
            # Solana private keys are expected to be a list of 64 bytes.
            # Convert the environment variable string (assumed to be base58 encoded) to this format.
            private_key_bytes = b58decode(private_key_str)
            self.wallet = Keypair.from_secret_key(private_key_bytes)
            self.public_key = self.wallet.public_key

            print(f"Wallet {str(self.public_key)} loaded")
        else:
            print("No private key provided, read-only mode")

        # Test connection to the blockchain
        try:
            version = self.client.get_version()
            print(f"Connected to Solana RPC. Version: {version['data']['solana-core']}")
        except Exception as e:
            print(f"Failed to connect to the Solana RPC: {e}")

        return self.client
