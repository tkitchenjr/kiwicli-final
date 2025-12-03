from database import Base
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

class Portfolio(Base):
    # def __init__(self, portfolio_id: int, name: str, description: str, holdings: list[Investment]):
    #     self.portfolio_id = portfolio_id
    #     self.name = name
    #     self.description = description
    #     self.holdings = holdings
    __tablename__ = "Portfolios"
    portfolio_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)    
    holdings: Mapped[str] = mapped_column(String(1000), nullable=True)
    owner: Mapped[str] = mapped_column(String(50), ForeignKey("Users.username"), nullable=False) 

def __str__(self):
    return f"Portfolio(portfolio_id={self.portfolio_id}, name={self.name}, description={self.description}, holdings={self.holdings})"
