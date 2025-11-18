# define starting user dictionary


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain.User import User


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

# Centralized session state: currently logged-in user object (or None)
current_user = None

# --- Helper functions: users and portfolio IDs ---
def username_exists(username: str) -> bool:
    return any(u.get("username", "").strip().lower() == username.strip().lower() for u in users)

def add_user_record(username: str, password: str, firstname: str, lastname: str, balance: float) -> None:
    users.append({
        "username": username,
        "password": password,
        "firstname": firstname,
        "lastname": lastname,
        "balance": balance,
    })

def next_portfolio_id() -> int:
    return (max([p.get("portfolio_id", 0) for p in portfolios], default=0) + 1) if portfolios else 1

#create query user method
def query_user(username: str):
    # Import User here to avoid circular import at module level
    from domain.User import User
    for user in users:
        if user["username"] == username:
            return User(**user)
    return None

def delete_user(username: str) -> bool:
    """
    Deletes a user by username. Returns True if deleted, False if not found or blocked.
    Admin account cannot be deleted. User cannot be deleted if they own any portfolios.
    """
    if username.strip().lower() == "admin":
        return False
    # Block deletion if user owns any portfolios
    if any(p.get("owner") == username for p in portfolios):
        return "has_portfolios"
    idx = next((i for i, u in enumerate(users) if u.get("username") == username), None)
    if idx is None:
        return False
    del users[idx]
    return True

#create Portfolio list
portfolios = [
    {
        "portfolio_id": 1,
        "name": "Tech Stocks",
        "description": "Stock & Crypto Holdings",
        "owner": "admin",
        "cash": 0.0,
        "holdings": {"AAPL": 10, "MSFT": 5, "AMZN": 2, "NVDA": 8, "BTC": 1}
    }
]
#create Security list
Securities = [
    {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "price": 250.00,
        "issuer": "CME"
    },
    {
        "symbol": "MSFT",
        "name": "Microsoft Corporation",
        "price": 500.00,
        "issuer": "CME"
    },
    {
        "symbol": "AMZN",
        "name": "Amazon",
        "price": 280.00,
        "issuer": "CME"
    },  
    {
        "symbol": "NVDA",
        "name": "Microsoft Corporation",
        "price": 200.00,
        "issuer": "CME"
    },
    {
        "symbol": "BTC",
        "name": "Bitcoin",
        "price": 105000,
        "issuer": "CME"
    }
]
