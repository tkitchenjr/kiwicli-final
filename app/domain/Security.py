#Define Securities class

class Security():
    def __init__(self, ticker:str, issuer:str, price: float):
        self.ticker = ticker
        self.issuer = issuer
        self.reference_price = price