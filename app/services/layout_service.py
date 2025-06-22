from flask import request
from werkzeug.datastructures import FileStorage
from app.models.user import User
from app.extensions import db
from app.schemas.layout_schema import UserProfileUpdateResult
from app.utils.image_utils import save_uploaded_image

def update_user_profile(
    user_id: int,
    name: str,
    intro: str,
    avatar_file: FileStorage = None,
    fallback_avatar: str = ''
) -> UserProfileUpdateResult:
    # 1. 头像上传处理
    if avatar_file:
        relative_path, avatar_url = save_uploaded_image(
            file=avatar_file,
            sub_folder='user/avatars'
        )
    else:
        relative_path = fallback_avatar.replace(request.host_url.rstrip('/'), '')
        avatar_url = fallback_avatar

    # 2. 更新数据库
    user = db.session.get(User, user_id)
    user.nickname = name
    user.signature = intro
    user.avatar = relative_path
    db.session.commit()

    # 3. 返回结构化数据（绝对路径给前端）
    return UserProfileUpdateResult(
        avatar=avatar_url,
        nickname=user.nickname,
        signature=user.signature
    )
