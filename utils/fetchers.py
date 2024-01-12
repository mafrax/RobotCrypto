import json
import asyncio
import aiohttp

async def fetch_abi_from_etherscan(token_address, etherscan_api_key, max_retries=5, retry_delay=5):
    """
    Fetches the ABI for a given token address from Etherscan.
    """
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

# You can add more fetching functions here as needed.
