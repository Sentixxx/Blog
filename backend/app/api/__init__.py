from .admin import admin
from .system import system
from .book import book

DEFAULT_BLUEPRINTS = [
    (admin,''),
    (system,''),
    (book,'/book')
]

def config_blueprint(app):
    for blueprint,url_prefix in DEFAULT_BLUEPRINTS:
        print(f'Registering blueprint `{blueprint.name}` with url prefix {url_prefix}')
        app.register_blueprint(blueprint,url_prefix=url_prefix)

