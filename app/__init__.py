import os
from flask import Flask
from dotenv import load_dotenv  # 自动加载 .env 文件
from .config import DevelopmentConfig, ProductionConfig
from .extensions import db, migrate, cors, jwt
from .controllers import register_blueprints
from .core.exceptions import register_error_handlers

# 加载 .env 文件
load_dotenv()

# 统一项目根目录
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(BASE_DIR, 'static'),  # 统一指定静态目录绝对路径
        static_url_path='/static',  # 访问URL前缀仍然是 /static
    )

    print("当前工作目录:", os.getcwd())
    print("静态文件目录:", app.static_folder)

    # 自动根据环境变量切换配置
    env = os.getenv(
        "FLASK_ENV", "development"
    )  # FLASK_ENV 用于判断当前运行模式，第二个参数载入不同的配置类（例如：是否开启调试、数据库连接、JWT密钥等）
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": "*",
                "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                ],  # 允许发送 application/json 类型的数据（表单/JSON 请求），允许携带token
                "supports_credentials": True,  # 允许跨域请求时携带登录凭证
            }
        },
    )
    jwt.init_app(app)

    # 注册蓝图
    register_blueprints(app)

    # 注册异常处理器
    register_error_handlers(app)

    return app
