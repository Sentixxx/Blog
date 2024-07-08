from .admin import admin

DEFAULT_BLUEPRINTS = [
    (admin,''),
]

def config_blueprint(app):
    for blueprint,url_prefix in DEFAULT_BLUEPRINTS:
        print(f'Registering blueprint `{blueprint.name}` with url prefix {url_prefix}')
        app.register_blueprint(blueprint,url_prefix='')

