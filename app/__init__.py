from flask import Flask
from app.db import db

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    #register extensions
    db.init_app(app)

    return app