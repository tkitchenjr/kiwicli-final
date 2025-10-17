# Define Investment Class

class Investment():
    def __init__(self, ticker: str, quantity:int, purchase_price:float):
        self.ticker = ticker
        self.quantity = quantity
        self.purchase_price = purchase_price