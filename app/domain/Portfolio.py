from __future__ import annotations
from database import Base
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING: import Investment

class Portfolio(Base):
    # def __init__(self, portfolio_id: int, name: str, description: str, holdings: list[Investment]):
    #     self.portfolio_id = portfolio_id
    #     self.name = name
    #     self.description = description
    #     self.holdings = holdings
    __tablename__ = "Portfolio"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)    
    owner: Mapped[str] = mapped_column(String(50), ForeignKey("User.username"), nullable=False)

    # map relationship to Investment lists DOES NOT NEED A COLUMN IN SQL TABLE
    # Intent is to serve as an ORM feature to access related Investment objects that I've designed to be held in holdings within a portfolio
    holdings: Mapped[list["Investment"]] = relationship("Investment", back_populates="holdings")
    

def __str__(self):
    return f"Portfolio(id={self.id}, name={self.name}, description={self.description}, holdings={self.holdings})"