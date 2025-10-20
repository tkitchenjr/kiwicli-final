from dataclasses import dataclass


@dataclass
class Portfolio:
    id: int
    name: str
    description: str
    holdings: dict