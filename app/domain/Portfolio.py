from dataclasses import dataclass


@dataclass
class Portfolio:
    def __init__(self, portfolio_id: int, name: str, description: str, holdings: list):
        self.portfolio_id = portfolio_id
        self.name = name
        self.description = description
        self.holdings = holdings