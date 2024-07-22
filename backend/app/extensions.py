from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def config_extensions(app):
    with app.app_context():
        db.init_app(app)
        print("db init success")