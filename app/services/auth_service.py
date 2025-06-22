from flask import current_app
from ..models.user import User
from ..extensions import db
from ..core.auth import generate_jwt
from ..utils.password_utils import hash_password, check_password
from ..core.exceptions import APIException

def login_or_register_service(phone: str, password: str):
    user = db.session.query(User).filter_by(phone=phone).first()

    if user:
        if not user.password:
            raise APIException("该账号未设置密码", code=40002)

        if not check_password(password, user.password):
            raise APIException("账号或密码错误，请重试", code=40003)
    else:
        hashed = hash_password(password)
        user = User(
            phone=phone,
            password=hashed,
            role='user',
            nickname=phone[:3] + '****',
            avatar='/static/assets/avatars/icons8-user-pulsar-color-32.png'
        )
        db.session.add(user)
        db.session.commit()
        current_app.logger.info(f"新用户注册成功：{phone}")

    token = generate_jwt(user.id)
    return user, token
