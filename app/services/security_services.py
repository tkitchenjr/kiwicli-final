from app.domain.Security import Security
from app.db import db

def view_all_securities() -> dict:
    try:
        session = db.session
        securities = session.query(Security).all()
        security_data = [
        {
            "Ticker": security.symbol,
            "Issuer": security.issuer,
            "Name": security.name,
            "Price": float(security.price),
        }
        for security in securities
        ]
        return {
            "success": True,
            "data": security_data,
            "status": 200
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error viewing securities {str(e)}",
            "status": 500
        }

# depricated all other previous functions including: place order