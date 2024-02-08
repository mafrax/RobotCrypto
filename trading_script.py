import json
import sys
import time
import os
import logging
from web3 import Web3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("web3").setLevel(logging.WARNING)  # Set Web3 logs to WARNING level

# Constants
UNISWAP_FACTORY_ADDRESS = '0x9Ad6C38BE94206cA50bb0d90783181662f0Cfa10'
UNISWAP_FACTORY_ABI_PATH = './traderjoe_abi.json'
WEB3_PROVIDER_URL = "https://api.avax.network/ext/bc/C/rpc"


# Utility Functions
def fetch_pool_reserves(pool_contract):
    return pool_contract.functions.getReserves().call()


def calculate_token_price(reserves, pair_info):
    # Identify which token is WAVAX and adjust the calculation accordingly
    if pair_info[0]['symbol'] == 'WAVAX':
        token_price = reserves[1] / reserves[0]  # Price of token1 in terms of WAVAX
    elif pair_info[1]['symbol'] == 'WAVAX':
        token_price = reserves[0] / reserves[1]  # Price of token0 in terms of WAVAX
    else:
        logging.error("Neither of the tokens in the pair is WAVAX.")
        return None
    return token_price


def display_pair_info(pair_info):
    for token in pair_info:
        logging.info(
            f"-----\nToken Address: {token['address']}\nSymbol: {token['symbol']}\nLiquidity: {token['liquidity']}\nHas ABI: {'Yes' if token['has_abi'] else 'No'}\nPotential Honeypot Risk: {'Yes' if token['is_potential_honeypot'] else 'No'}\n-----")


def load_abi(file_name):
    try:
        script_directory = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_directory, file_name)
        with open(file_path, 'r') as abi_file:
            return json.load(abi_file)
    except Exception as e:
        logging.error(f"Error loading ABI file: {e}")
        raise


def main(pair_info_json):
    try:
        private_key = os.getenv("PRIVATE_KEY")
        if not private_key:
            raise Exception("Private key not found. Make sure PRIVATE_KEY is set.")

        web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
        uniswap_factory_abi = load_abi('traderjoe_abi.json')
        factory_contract = web3.eth.contract(address=UNISWAP_FACTORY_ADDRESS, abi=uniswap_factory_abi)

        account = web3.eth.account.from_key(private_key)
        logging.info(f"Loaded account: {account.address}")

        pair_info = json.loads(pair_info_json)
        display_pair_info(pair_info)

        token0_address = pair_info[0]['address']
        token1_address = pair_info[1]['address']
        pool_address = factory_contract.functions.getPair(token0_address, token1_address).call()
        pool_contract = web3.eth.contract(address=pool_address, abi=uniswap_factory_abi)

        while True:
            reserves = fetch_pool_reserves(pool_contract)
            # Updated to use the modified price calculation function
            price = calculate_token_price(reserves, pair_info)
            if price is not None:
                logging.info(f"Current price relative to WAVAX: {price}")
            time.sleep(10)
    except Exception as e:
        logging.error(f"Error in main function: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Usage: python script.py <pair_info_json>")
        sys.exit(1)

    pair_info_json = sys.argv[1]
    main(pair_info_json)
