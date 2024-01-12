import asyncio
from utils.fetchers import fetch_abi_from_etherscan
from models.token import Token
import logging

class EventListener:
    def __init__(self, uniswap_contract, web3, etherscan_api_key):
        logging.debug("Initializing EventListener")
        self.uniswap_contract = uniswap_contract
        self.web3 = web3
        self.etherscan_api_key = etherscan_api_key

    async def handle_event(self, event):
        print('\nPair Created Event Detected')

        # Fetch token details using token.py
        token0 = Token(self.web3, event.args.token0)
        token1 = Token(self.web3, event.args.token1)
        token0_symbol = token0.get_symbol()
        token1_symbol = token1.get_symbol()

        print(f"Pair: {token0_symbol} - {token1_symbol}")

        # Fetch ABIs for the tokens
        token0_abi = await fetch_abi_from_etherscan(event.args.token0, self.etherscan_api_key)
        token1_abi = await fetch_abi_from_etherscan(event.args.token1, self.etherscan_api_key)

        if token0_abi and token1_abi:
            print(f"ABIs fetched for tokens: {event.args.token0}, {event.args.token1}")

    async def listen_to_events(self):
        logging.debug("Listening to events")

        try:
            event_filter = self.uniswap_contract.contract.events.PairCreated.create_filter(fromBlock='latest')
            logging.debug(f"Event Filter: {event_filter}")
        except AttributeError as e:
            logging.error(f"Error creating event filter: {e}")
            return
        while True:
            for event in event_filter.get_new_entries():
                await self.handle_event(event)
            await asyncio.sleep(2)  # Polling interval
