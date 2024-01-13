import asyncio
import json
from utils.fetchers import fetch_abi_from_etherscan
from safetycheck.honeypot_checks import check_abi_for_honeypot_risks  # Import the function
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

        print(f"\nPair: {token0_symbol} : {event.args.token0} - {token1_symbol} : {event.args.token1}")

        # Fetch liquidity information
        pair_address = event.args.pair
        token0 = Token(self.web3, event.args.token0)
        token1 = Token(self.web3, event.args.token1)

        token0_liquidity = token0.get_balance(pair_address)
        token1_liquidity = token1.get_balance(pair_address)

        print(f"\nLiquidity - {token0_symbol}: {token0_liquidity}, {token1_symbol}: {token1_liquidity}")

        # Fetch ABIs for the tokens
        token0_abi = await fetch_abi_from_etherscan(event.args.token0, self.etherscan_api_key)
        token1_abi = await fetch_abi_from_etherscan(event.args.token1, self.etherscan_api_key)

        if token0_abi and token1_abi:
            print(f"ABIs fetched for tokens: {event.args.token0}, {event.args.token1}")

        # Check ABIs for potential honeypot risks
            token0_risk = check_abi_for_honeypot_risks(token0_abi)
            token1_risk = check_abi_for_honeypot_risks(token1_abi)

            if token0_risk or token1_risk:
                print("Warning: Potential honeypot risks detected in one of the tokens.")
            else:
                print("No immediate honeypot risks detected in ABIs.")

    async def listen_to_events(self):
        logging.debug("Listening to events")

        try:
            event_filter = self.uniswap_contract.contract.events.PairCreated.create_filter(fromBlock='latest')
            logging.debug(f"Event Filter: {event_filter}")
        except AttributeError as e:
            logging.error(f"Error creating event filter: {e}")
            return

        while True:
            try:
                new_entries = event_filter.get_new_entries()
                for event in new_entries:
                    # Handle event
                    await self.handle_event(event)

            except ValueError as e:
                logging.error(f"ValueError encountered: {e}")
                logging.warning("Filter not found or other error, recreating filter")
                try:
                    event_filter = self.uniswap_contract.contract.events.PairCreated.create_filter(fromBlock='latest')
                except Exception as e:
                    logging.error(f"Error recreating event filter: {e}")
                    await asyncio.sleep(10)  # Wait longer before retrying to prevent rapid failure loops
                    continue
            await asyncio.sleep(2)  # Adjust the duration as needed
