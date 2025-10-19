# define starting user dictionary

from domain.User import User
from domain.Portfolio import Portfolio
from domain.Security import Security


#create User list
users = [
    {
        "username": "admin",
        "password": "admin",
        "firstname": "Admin",
        "lastname": "Admin",
        "balance": 100000.00
    }
]

#create query user method
def query_user(username: str) -> User|None:
    for user in users:
        if user["username"] == username:
            return User(**user)
    return None

#create Portfolio list
portfolios = [
    {
        "portfolio_id": 1,
        "name": "Tech Stocks",
        "description": "Stock & Crypto Holdings",
        "holdings": {"AAPL,MSFT,AMZN,NVDA,BTC"}
    }
]
#create Security list
Securities = [
    {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "price": 250.00},
    {
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "price": 500.00},
    {
        "symbol": "AMZN",
        "name": "Amazon",
        "price": 280.00},  
    {
        "symbol": "NVDA",
        "name": "Microsoft Corporation",
        "price": 200.00},
    {
        "symbol": "BTC",
        "name": "Bitcoin",
        "price": 105000}
]
