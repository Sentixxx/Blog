from app import create_app
from app.extensions import db


config_name = "development"
def print_routes(app):
    for rule in app.url_map.iter_rules():
        print(f'Endpoint: {rule.endpoint}, URL: {rule.rule}, Methods: {list(rule.methods)}')

app = create_app()

# print_routes(app)

from flask import current_app

# def check_db_connection():
#     try:
#         # 尝试执行一个简单的查询
#         with current_app.app_context():
#             conn = db.engine.connect()
#             conn.execute("SELECT 1")
#         print("Database connection is OK.")
#     except Exception as e:
#         print(f"Database connection failed: {e}")
#         raise
if __name__ == '__main__':
        app.run(host = '0.0.0.0',port=8090,debug=True)

