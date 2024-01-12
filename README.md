# Uniswap Pair Monitor

## Overview

This program is a Python application designed to interact with Uniswap contracts on the Ethereum blockchain. It utilizes the Web3.py library to connect to the blockchain, monitor new liquidity pair creations, fetch token symbols, and gather liquidity data. Additionally, the program employs asynchronous programming to efficiently handle network requests and blockchain event monitoring.

## Features

- **Connect to Blockchain**: Utilizes Infura for an Ethereum blockchain connection.
- **Monitor Uniswap Pairs**: Listens for the creation of new Uniswap liquidity pairs.
- **Fetch Token Information**: Retrieves token symbols for new pairs.
- **Get Liquidity Data**: Extracts liquidity data for new pairs.
- **Asynchronous ABI Fetching**: Asynchronously fetches the ABI (Application Binary Interface) from Etherscan for tokens.

## Prerequisites

Before running this program, you will need:

- Python 3.6 or higher.
- Access to an Ethereum node (via Infura or another provider).
- An Etherscan API key (for fetching token ABIs).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone [repository URL]
   cd [repository directory]
   ```

2. **Set up a Virtual Environment** (Optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Replace the placeholder values in the script with your actual Infura URL and Etherscan API key:

- `infura_url`: Your Infura project URL.
- `etherscan_api_key`: Your Etherscan API key.

## Usage

Run the script using Python:

```bash
python3 path_to_script.py
```

The program will start monitoring the Uniswap contracts for new pair creations and output information about them.

## How It Works

- The script connects to the Ethereum blockchain using Web3.py with an HTTP provider.
- It listens for the `PairCreated` event on the Uniswap Factory contract.
- When a new pair is created, it fetches the symbols of the tokens in the pair and displays their liquidity.
- It also asynchronously fetches the ABIs for the new tokens from Etherscan.

## Important Notes

- The program is configured to work with the Avalanche network endpoint. Modify the `infura_url` to switch to a different Ethereum network.
- Always secure your API keys and do not expose them in public repositories.

## Troubleshooting

If you encounter any issues:

- Check your Python version with `python3 --version`.
- Ensure your virtual environment is activated (if you're using one).
- Verify that your Infura URL and Etherscan API key are correct.

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[Add your chosen license here]
