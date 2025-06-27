from flask import Blueprint, request
from ..core.response import Result
from ..core.exceptions import APIException
from ..services.auth_service import login_or_register_service

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/pwd', methods=['POST'])
def login_or_register():
    data = request.get_json()
    phone = data.get('phone')
    password = data.get('password')

    if not phone or not password:
        raise APIException("手机号和密码不能为空", code=40001)

    user, token = login_or_register_service(phone, password)
    avatar_url = request.host_url.rstrip('/') + user.avatar

    return Result.success(
        {
            "user": {
                "id": user.id,
                "phone": user.phone,
                "role": user.role,
                "nickname": user.nickname,
                "avatar": avatar_url,
                "become_author_at": (
                    user.become_author_at.strftime("%Y-%m-%d %H:%M:%S")
                    if user.become_author_at
                    else ""
                ),
                "signature": user.signature,
                "level": user.level,
            },
            "token": token,
        }
    )
