import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    # 通用配置
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:123456@localhost:3306/cms?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭对模型修改的监控
    JSON_AS_ASCII = False  # 解决 jsonify 中文乱码问题

    # JWT 配置（如使用 flask-jwt-extended 或自定义）
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
