from app.domain.Portfolio import Portfolio
from app.domain.User import User
from app.db import db

def view_users() -> dict:
    try:
        session = db.session
        users = session.query(User).all()
        user_data = [
            {
            "username": user.username,
            "password": user.password,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "balance": user.balance,
            }
        for user in users
        ]
        return {
            "success": True,
            "data": user_data,
            "status": 200
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error viewing securities {str(e)}",
            "status": 500
        }
    
def get_user_by_id(username:str) -> dict:
    try:
        session = db.session
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return {
                "success": False,
                "message": f"No portfolios found for {user} with Portfolio Id {id}",
                "status": 404
            }
        else:
            user_data= {
                "username": user.username,
                "password": user.password,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "balance": user.balance,
                }
            return {
                "success": True,
                "message": f"User {user} returned.",
                "data": user_data,
                "status": 200
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error getting User by id: {str(e)}",
            "status": 500
        }

def create_user(username: str, password: str, firstname: str, lastname: str , balance: float ) -> dict:
    user = User(username=username, password=password, firstname=firstname, lastname=lastname, balance=balance)
    try:
        session = db.session
        session.add(user)
        session.commit()

        return {
            "success": True,
            "message": f"User {username} created.",
            "username": username,
            "status": 201
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating user: {str(e)}",
            "status": 500
        }
    

def delete_user(username: str) -> dict:
    try:
        session = db.session
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return {
                "success": False,
                "message": f"User {username} not found.",
                "status": 404
            }
        if user == "admin" or "Admin":
            return {
                "success": False,
                "message": f"Cannot delete Admin",
                "status":400
            }
        if session.query(Portfolio).filter_by(owner=username).first():
            return {
                "success": False,
                "message": "User cannot be deleted with active portfolios. Delete portfolios first.",
                "status": 400
            }
        session.delete(user)
        session.commit()
        return {
            "success": True,
            "message": f"User '{username}' deleted successfully.",
            "status": 200
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error deleting portfolio: {str(e)}",
            "status": 500
        }
    
