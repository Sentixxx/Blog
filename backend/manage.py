from app import create_app

import os

config_name = "development"
def print_routes(app):
    for rule in app.url_map.iter_rules():
        print(f'Endpoint: {rule.endpoint}, URL: {rule.rule}, Methods: {list(rule.methods)}')

app = create_app()
# print_routes(app)

if __name__ == '__main__':
    app.run(host = '127.0.0.1',port=8090,debug=True)

