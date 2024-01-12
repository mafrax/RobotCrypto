# import the following dependencies
import json
from web3 import Web3
import asyncio
import aiohttp

# add your blockchain connection information
infura_url = 'https://api.avax.network/ext/bc/C/rpc'
web3 = Web3(Web3.HTTPProvider(infura_url))

# uniswap address and abi
uniswap_router = '0x60aE616a2155Ee3d9A68541Ba4544862310933d4'
uniswap_factory = '0x9Ad6C38BE94206cA50bb0d90783181662f0Cfa10'
uniswap_factory_abi = json.loads(
    '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

contract = web3.eth.contract(address=uniswap_factory, abi=uniswap_factory_abi)


async def fetch_abi_from_etherscan(token_address, max_retries=5, retry_delay=5):
    etherscan_api_key = 'DCMEWAPI5F8NJMPP4CB9ZVAAQH2GBYHXCS'
    etherscan_url = f'https://api.routescan.io/v2/network/mainnet/evm/43114/etherscan/api?module=contract&action=getabi&address={token_address}&apikey={etherscan_api_key}'

    retries = 0
    while retries < max_retries:
        async with aiohttp.ClientSession() as session:
            async with session.get(etherscan_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['status'] == '1':
                        return json.loads(data['result'])
                retries += 1
                await asyncio.sleep(retry_delay)

    print(f"Failed to fetch ABI for {token_address} after {max_retries} retries.")
    return None


def get_token_symbol(token_address):
    try:
        token_abi = json.loads(
            '[{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]')
        token_contract = web3.eth.contract(address=token_address, abi=token_abi)
        return token_contract.functions.symbol().call()
    except Exception as e:
        print(f"Error getting symbol for token at {token_address}: {e}")
        return None


def get_pair_contract(pair_address):
    try:
        pair_abi = json.loads(
            '[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"reserve0","type":"uint112"},{"internalType":"uint112","name":"reserve1","type":"uint112"},{"internalType":"uint32","name":"blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"}]')
        return web3.eth.contract(address=pair_address, abi=pair_abi)
    except Exception as e:
        print(f"Error creating contract instance for pair at {pair_address}: {e}")
        return None


def get_liquidity(pair_contract):
    try:
        reserves = pair_contract.functions.getReserves().call()
        return reserves
    except Exception as e:
        print(f"Error getting liquidity for pair: {e}")
        return (None, None)


async def handle_event(event):
    print('\n pair_created event')
    token0_address = event.args.token0
    token1_address = event.args.token1
    pair_address = event.args.pair

    token0_symbol = get_token_symbol(token0_address)
    token1_symbol = get_token_symbol(token1_address)

    if token0_symbol is not None and token1_symbol is not None:
        print(f"New Pair Created: {token0_symbol}-{token1_symbol} ({token0_address}, {token1_address})")

    pair_contract = get_pair_contract(pair_address)
    if pair_contract is not None:
        reserves = get_liquidity(pair_contract)
        if reserves[0] is not None and reserves[1] is not None:
            print(f"Liquidity - Token0: {reserves[0]}, Token1: {reserves[1]}")

    # Start ABI fetching tasks without awaiting their results immediately
    token0_abi_task = asyncio.create_task(fetch_abi_from_etherscan(token0_address))
    token1_abi_task = asyncio.create_task(fetch_abi_from_etherscan(token1_address))

    # Optionally, wait for ABI tasks later or elsewhere in your code
    token0_abi = await token0_abi_task
    token1_abi = await token1_abi_task

    # Use ABIs if available
    if token0_abi and token1_abi:
        print(f"Got ABIs for tokens: {token0_address}, {token1_address}")


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    print("Waiting for new pair...")

    while True:
        for PairCreated in event_filter.get_new_entries():
            await handle_event(PairCreated)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.PairCreated.create_filter(fromBlock='latest')
    # block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    # loop = asyncio.get_event_loop()
    # try:
    # loop.run_until_complete(
    # asyncio.gather(
    #     log_loop(event_filter, 2)))
    asyncio.run(log_loop(event_filter, 2))
    # log_loop(block_filter, 2),
    # log_loop(tx_filter, 2)))
    # finally:
    # close loop to free up system resources
    # loop.close()


if __name__ == "__main__":
    main()