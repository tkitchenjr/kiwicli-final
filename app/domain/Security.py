from database import Base
from sqlalchemy import ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column

class Security:
    # def __init__(self, symbol: str, name: str, sector: str):
    #     self.symbol = symbol
    #     self.name = name
    #     self.price = price
    #     self.issuer = issuer
    __tablename__ = "Securities"
    symbol: Mapped[str] = mapped_column(String(10), ForeignKey("Investments.ticker"), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[str] = mapped_column(Float(50), nullable=False)
    issuer: Mapped[str] = mapped_column(String(100), nullable=False)

def __str__(self):
    return f"Security(symbol={self.symbol}, name={self.name}, price={self.price})"