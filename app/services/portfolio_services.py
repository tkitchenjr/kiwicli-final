from app.domain.Investment import Investment
from app.domain.Portfolio import Portfolio
from app.domain.Security import Security
from app.db import db


def view_all_portfolios() -> dict:
    try:
        session = db.session
        portfolios = session.query(Portfolio).all()
        portfolio_data = [
                {
                "id": portfolio.id,
                "name": portfolio.name,
                "description": portfolio.description,
                "owner": portfolio.owner
                }
            for portfolio in portfolios
            ]
        return {
                "success": True,
                "data": portfolio_data,
                "status": 200
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error getting portfolios {str(e)}",
            "status": 500
        }   

        
        
def get_portfolio_by_id(id:int) -> dict:
    try: 
        session = db.session
        portfolio = session.query(Portfolio).filter_by(id=id).first()

        if not portfolio:
            return {
                "success": False,
                "message": f"Portfolio Id {id} not found!",
                "status": 404
            }
        else:
            portfolio_data = {
                "id": portfolio.id,
                 "name": portfolio.name,
                 "description": portfolio.description,
                 "owner": portfolio.owner,
                }

            return {
                "success": True,
                "message": f"Portfolio {id} returned.",
                "data": portfolio_data,
                "status": 200
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error retrieving Portfolios: {str(e)}",
            "status": 500
        }
    


def create_portfolio(name: str, description: str, owner: str) -> dict:
    
    portfolio = Portfolio(name=name, description=description, owner=owner)
    
    try:
        session = db.session
        session.add(portfolio)
        session.commit()

        return {
            "success": True,
            "message": f"Portfolio '{name}' created successfully.",
            "portfolio_id": portfolio.id,
            "status": 201
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating portfolio: {str(e)}",
            "status": 500
        }
 
    
    
def delete_portfolio(portfolio_id: int) -> dict: 
    try:
        session = db.session
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id).first()
        if not portfolio:
            return {
                "success": False,
                "message": f"Portfolio {portfolio} not found.",
                "status": 404
            }
        
        if session.query(Investment).filter_by(portfolio_id=portfolio.id).first():
            return {
                "success": False,
                "message": "Cannot delete portfolio: investments must be liquidated before deletion.",
                "status": 400
            }
        session.delete(portfolio)
        session.commit()
        return {
            "success": True,
            "message": f"Portfolio '{portfolio.name}' deleted successfully.",
            "status": 200
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error deleting portfolio: {str(e)}",
            "status": 500
        }

def add_new_security(portfolio_id: int, ticker:str, qty:int) -> dict:
    try: 
        session = db.session
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id).first()
        security = session.query(Security).filter_by(symbol=ticker).first()
        if not security:
            return {
                    "success": False,
                    "message": f"Security {ticker} not found.",
                    "status": 404
                }
                
        if not portfolio:
            return {
                "success": False,
                "message": f"Portfolio {portfolio_id} not found.",
                "status": 400
            }
        investment = session.query(Investment).filter_by(portfolio_id=portfolio_id,Ticker=ticker).first()
        if investment:
            investment.Qty += qty
        else:
            investment = Investment(
                Ticker = ticker,
                portfolio_id = portfolio_id,
                Qty=qty,
                purchase_price =security.price,
            )
            session.add(investment)
        session.commit()
        return {
            "success": True,
            "message": f"{qty} of {security.name} added to Portfolio {portfolio_id}",
            "status": 200
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error adding Security: {str(e)}",
            "status": 500
        }


def harvest_investment(ticker: str, qty: int, portfolio_id: int) -> dict:
    try: 
        session = db.session
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id).first()
        if not portfolio:
            return {
                "success": False,
                "message": f"Portfolio {portfolio_id} not found.",
                "status": 404
            }
        investments = session.query(Investment).filter_by(ticker=ticker, id=portfolio_id).all()
        if not investments:
            return {
                "success": False,
                "message": "No holdings found to liquidate.",
                "status": 404
            }
        for investment in investments:
            if investment.Qty <= qty:
                return {
                    "success": False,
                    "message": f"Cannot liquidate more than owned quantity of {investment.Qty}.",
                    "status": 400
                }
            if investment.Qty >= qty:
                investment.Qty -= qty
                return {
                    "success": True,
                    "message": f"Liquidated {qty} of {investment.Ticker} successfully.",
                    "status": 200
                }
            if investment.Qty == qty:
                session.delete(investment)
                session.commit()
                return {
                    "success": True,
                    "message": f"Liquidated all holdings of {investment.Ticker} successfully.",
                    "status": 200
                }  
    except Exception as e:
        return {
            "success": False,
            "message": f"Error liquidating Investments: {str(e)}",
            "status": 500
        }

# depricated all other previous functions including: view_holdings, liquidate_holdings, partial_lidquidate_holdings
