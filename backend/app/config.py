import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# print (BASE_DIR)


class Config:
    DB_NAME = os.environ.get('DB_NAME') or 'book_admin'
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'root'
    DB_HOST = os.environ.get('DB_HOST') or '0.0.0.0'
    DB_PORT = os.environ.get('DB_PORT') or '3306'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
    JWT_SECRET_KEY = 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

class DevelopmentConfig(Config):
    DEBUG = True
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #查询时会显示原始SQL语句
    # SQLALCHEMY_ECHO = True
    # print(Config.SQLALCHEMY_DATABASE_URI)


config = {
    "development": DevelopmentConfig,
}