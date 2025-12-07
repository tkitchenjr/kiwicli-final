from database import Base
from sqlalchemy import ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column

class Security(Base):
    # def __init__(self, symbol: str, name: str, sector: str):
    #     self.symbol = symbol
    #     self.name = name
    #     self.price = price
    #     self.issuer = issuer
    __tablename__ = "Security"
    symbol: Mapped[str] = mapped_column(String(10), ForeignKey("Investment.Ticker"), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    issuer: Mapped[str] = mapped_column(String(10), nullable=False)

def __str__(self):
    return f"Security(symbol={self.symbol}, name={self.name}, price={self.price})"