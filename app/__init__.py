from flask import Flask
from app.db import db
from app.routes.login_routes import login_routes
from app.routes.user_routes import user_routes
from app.routes.portfolio_routes import portfolio_routes
from app.routes.security_routes import security_routes
from app.routes.transaction_routes import transaction_routes

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    #register extensions
    db.init_app(app)
    app.register_blueprint(login_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(portfolio_routes)
    app.register_blueprint(security_routes)
    app.register_blueprint(transaction_routes)

    return app
