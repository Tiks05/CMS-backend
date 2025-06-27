from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# 实例化扩展对象（不绑定 app）
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
