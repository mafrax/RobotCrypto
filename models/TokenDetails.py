class TokenDetails:
    def __init__(self, address, symbol, liquidity, has_abi, honeypot_risk):
        self.address = address
        self.symbol = symbol
        self.liquidity = liquidity
        self.has_abi = has_abi
        self.honeypot_risk = honeypot_risk
