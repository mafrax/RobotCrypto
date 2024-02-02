import asyncio
import json

from models.TokenDetails import TokenDetails
from utils.fetchers import fetch_abi_from_etherscan
from safetycheck.honeypot_checks import check_abi_for_honeypot_risks  # Import the function
from models.token import Token
import logging


class EventListener:
    def __init__(self, uniswap_contract, web3, etherscan_api_key, callback):
        logging.debug("Initializing EventListener")
        self.uniswap_contract = uniswap_contract
        self.web3 = web3
        self.etherscan_api_key = etherscan_api_key
        self.callback = callback  # A callback function to handle new pairs

    async def handle_event(self, event):
        print('\nPair Created Event Detected')

        # Fetch token details using token.py
        token0 = Token(self.web3, event.args.token0)
        token1 = Token(self.web3, event.args.token1)
        token0_symbol = token0.get_symbol()
        token1_symbol = token1.get_symbol()

        token0_decimals = token0.get_decimals()
        token1_decimals = token1.get_decimals()

        print(f"\nPair: {token0_symbol} : {event.args.token0}  - {token1_symbol} : {event.args.token1}")

        # Fetch liquidity information
        pair_address = event.args.pair

        token0_liquidity = token0.get_balance(pair_address)
        token1_liquidity = token1.get_balance(pair_address)

        token0_liquidity_formatted = token0.format_liquidity(token0_liquidity)
        token1_liquidity_formatted = token1.format_liquidity(token1_liquidity)

        print(f"\nLiquidity - {token0_symbol}: {token0_liquidity_formatted} {token0_decimals}, {token1_symbol}: {token1_liquidity_formatted} {token1_decimals}")

        # Fetch ABIs for the tokens
        token0_abi = await fetch_abi_from_etherscan(event.args.token0, self.etherscan_api_key)
        token1_abi = await fetch_abi_from_etherscan(event.args.token1, self.etherscan_api_key)

        token0_risk = True
        token1_risk = True

        if token0_abi and token1_abi:
            print(f"ABIs fetched for tokens: {token0_symbol}, {token1_symbol}")

            # Check ABIs for potential honeypot risks
            token0_risk = check_abi_for_honeypot_risks(token0_abi)
            token1_risk = check_abi_for_honeypot_risks(token1_abi)

            if token0_risk or token1_risk:
                print("Warning: Potential honeypot risks detected in one of the tokens.")
            else:
                print("No immediate honeypot risks detected in ABIs.")

        # Create TokenInfo objects
        token0_info = TokenDetails(event.args.token0, token0_symbol, token0_liquidity, bool(token0_abi),
                                   token0_risk)
        token1_info = TokenDetails(event.args.token1, token1_symbol, token1_liquidity, bool(token1_abi),
                                   token1_risk)

        return token0_info, token1_info

    async def listen_to_events(self):
        logging.debug("Listening to events")

        try:
            event_filter = self.uniswap_contract.contract.events.PairCreated.create_filter(fromBlock='latest')
            logging.debug(f"Event Filter: {event_filter}")
        except AttributeError as e:
            logging.error(f"Error creating event filter: {e}")
            return

        retry_count = 0
        max_retries = 5  # Set a maximum number of retries
        while True:
            try:
                new_entries = event_filter.get_new_entries()
                for event in new_entries:
                    pair_info = await self.handle_event(event)
                    await self.callback(pair_info)  # Call the callback with the new pair info

                retry_count = 0  # Reset retry count after successful operation

            except ValueError as e:
                logging.error(f"ValueError encountered: {e}")
                retry_count += 1
                if retry_count > max_retries:
                    logging.error("Maximum retries reached. Exiting.")
                    break

                logging.warning("Filter not found or other error, recreating filter with backoff")
                await asyncio.sleep(2 ** retry_count)  # Exponential backoff

                try:
                    event_filter = self.uniswap_contract.contract.events.PairCreated.create_filter(fromBlock='latest')
                    logging.debug(f"Event Filter recreated: {event_filter}")
                except Exception as e:
                    logging.error(f"Error recreating event filter: {e}")
                    await asyncio.sleep(10)
                    continue
