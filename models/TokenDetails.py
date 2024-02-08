class TokenDetails:
    def __init__(self, address, symbol, liquidity, has_abi, honeypot_risk):
        self.address = address
        self.symbol = symbol
        self.liquidity = liquidity
        self.has_abi = has_abi
        self.honeypot_risk = honeypot_risk

    def to_dict(self):
        return {
            "address": self.address,
            "symbol": self.symbol,
            "liquidity": self.liquidity,
            "has_abi": self.has_abi,
            "is_potential_honeypot": self.honeypot_risk
        }
