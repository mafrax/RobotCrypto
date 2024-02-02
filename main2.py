import asyncio
import json
import os
import subprocess
import shlex
import sys

from blockchain.connection import BlockchainConnection
from blockchain.contracts import UniswapFactoryContract
from blockchain.events import EventListener
from dotenv import load_dotenv

from models.token import Token
from utils.fetchers import fetch_abi_from_etherscan

import logging

# logging.basicConfig(level=logging.DEBUG)

INFURA_URL = 'https://api.avax.network/ext/bc/C/rpc'
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
UNISWAP_FACTORY_ADDRESS = '0x9Ad6C38BE94206cA50bb0d90783181662f0Cfa10'
UNISWAP_FACTORY_ABI = json.loads(
    '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

pairs = []  # List to store pairs


async def handle_new_pair(pair_info):
    pairs.append(pair_info)

    # Convert pair_info to a JSON string
    pair_info_json = json.dumps([pair_info[0].to_dict(), pair_info[1].to_dict()])

    # Properly escape the JSON string for AppleScript
    pair_info_json_escaped = pair_info_json.replace('"', '\\"')

    pair_info_arg = shlex.quote(pair_info_json_escaped)

    # Command to open a new Terminal window and execute the script
    command = f'tell application "Terminal" to do script "python3 /Users/marcmongin/PycharmProjects/pythonProject/trading_script.py {pair_info_arg}"'
    subprocess.run(["osascript", "-e", command])

    print(f"New pair added: {pair_info}")


async def main():
    # Initialize blockchain connection
    blockchain_connection = BlockchainConnection()
    web3 = blockchain_connection.connect()

    # Initialize and start event listener
    uniswap_factory_contract = UniswapFactoryContract(web3, UNISWAP_FACTORY_ADDRESS)
    event_listener = EventListener(uniswap_factory_contract, web3, ETHERSCAN_API_KEY, handle_new_pair)
    await event_listener.listen_to_events()

    # After listen_to_events ends
    print("Pairs found:", pairs)


if __name__ == "__main__":
    asyncio.run(main())
