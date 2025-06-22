import jwt
from datetime import datetime, timedelta
from flask import current_app

# 生成 JWT Token
def generate_jwt(user_id: int, expires: int = 3600) -> str: # expires 为过期时间，单位为秒
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=expires)
    }
    secret = current_app.config["SECRET_KEY"]
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token
