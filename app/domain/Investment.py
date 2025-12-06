from database import Base
from __future__ import annotations
from sqlalchemy import ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING: import Portfolio

class Investment(Base):
    # def __init__(self, ticker: str, qty: int, purchase_price: float):
    #     self.ticker =ticker
    #     self.qty =qty
    #     self.purchase_price =purchase_price
    __tablename__ = "Investment"
    Ticker: Mapped[str] = mapped_column(String(10), primary_key=True, nullable=False)
    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("Portfolio.id"), nullable=False)
    Qty: Mapped[int] = mapped_column(Integer, nullable=False)
    purchase_price: Mapped[float] = mapped_column(Float, nullable=False)
    
    #relationship back to Portfolio
    holdings: Mapped["Portfolio"] = relationship("Portfolio", back_populates="holdings")

def __str__(self):
    return f"Investment(ticker={self.Ticker}, portfolio_id={self.portfolio_id}, qty={self.Qty}, purchase_price={self.purchase_price})"