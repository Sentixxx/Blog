from flask import Flask
from app.api import config_blueprint
from app.extensions import config_extensions
from flask_jwt_extended import JWTManager
from app.models import init_db_table
from app.config import config



def create_app():

    app = Flask(__name__)
    # CORS(app, supports_credentials=True)
    
    app.config.from_object(config["development"])

    config_extensions(app)

    config_blueprint(app)
    # with app.app_context():
    #     init_db_table()

    return app
