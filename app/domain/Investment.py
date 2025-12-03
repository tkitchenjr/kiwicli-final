from database import Base
from sqlalchemy import ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

class Investment(Base):
    # def __init__(self, ticker: str, qty: int, purchase_price: float):
    #     self.ticker =ticker
    #     self.qty =qty
    #     self.purchase_price =purchase_price
    __tablename__ = "Investments"
    ticker: Mapped[str] = mapped_column(String(10), primary_key=True, nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    purchase_price: Mapped[float] = mapped_column(Float, nullable=False)
    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("Portfolios.portfolio_id"), nullable=False)

def __str__(self):
    return f"Investment(ticker={self.ticker}, qty={self.qty}, purchase_price={self.purchase_price})"