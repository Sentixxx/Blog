from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

jwt = JWTManager()
db = SQLAlchemy()

def config_extensions(app):
    with app.app_context():
        db.init_app(app)
        print("db init success")
        jwt.init_app(app)
        print("jwt init success")