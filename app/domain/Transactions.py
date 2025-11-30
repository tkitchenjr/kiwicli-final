class Transactions(): 
    def __init__(self, transaction_id: str, user_id: str, portfolio_id: str, security_id: str, transaction_type: str, qty: int, price: float, timestamp: str):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.portfolio_id = portfolio_id
        self.security_id = security_id
        self.transaction_type = transaction_type
        self.qty = qty
        self.price = price
        self.timestamp = timestamp
        