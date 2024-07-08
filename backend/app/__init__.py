from flask import Flask
from app.api import config_blueprint
from app.extensions import config_extensions
from app.config import config

def create_app():

    app = Flask(__name__)

    app.config.from_object(config["development"])

    config_extensions(app)

    config_blueprint(app)

    return app