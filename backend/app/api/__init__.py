from .admin import admin

DEFAULT_BLUEPRINTS = [
    (admin,'/api/admin'),
]

def config_blueprint(app):
    for blueprint,url_prefix in DEFAULT_BLUEPRINTS:
        app.register_blueprint(blueprint,url_prefix=url_prefix)