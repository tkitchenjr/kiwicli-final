from database import Base
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

class Transactions(Base): 
    # def __init__(self, transaction_id: str, user_id: str, portfolio_id: str, security_id: str, transaction_type: str, qty: int, price: float, timestamp: str):
    #     self.transaction_id = transaction_id
    #     self.user_id = user_id
    #     self.portfolio_id = portfolio_id
    #     self.security_id = security_id
    #     self.transaction_type = transaction_type
    #     self.qty = qty
    #     self.price = price
    #     self.timestamp = timestamp
    __tablename__ = "Transactions"
    transaction_id: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False)
    user_id: Mapped[str] = mapped_column(String(50), nullable=False)
    portfolio_id: Mapped[str] = mapped_column(String(50), nullable=False)
    security_id: Mapped[str] = mapped_column(String(50), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(20), nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[str] = mapped_column(String(50), nullable=False)

def __str__(self):
    return f"Transactions(transaction_id={self.transaction_id}, user_id={self.user_id}, portfolio_id={self.portfolio_id}, security_id={self.security_id}, transaction_type={self.transaction_type}, qty={self.qty}, price={self.price}, timestamp={self.timestamp})"