from flask import Flask
from app.db import db
from app.routes.user_routes import user_bp
from app.routes.portfolio_routes import portfolio_bp
from app.routes.security_routes import security_bp


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    #register extensions
    db.init_app(app)

    #register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(security_bp)

    return app
