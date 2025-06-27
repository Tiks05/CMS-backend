from flask import Blueprint, request
from ..schemas.layout_schema import UserProfileUpdateForm, SearchBookRequest
from ..services.layout_service import update_user_profile, search_books
from ..core.response import Result

layout_bp = Blueprint('layout', __name__)


@layout_bp.route('/profile/update', methods=['POST'])
def update_profile():
    form = request.form
    avatar_file = request.files.get('avatar')  # 上传的新头像（可为空）

    # 使用 Pydantic 校验字段：id、avatar、nickname、introduction
    data = UserProfileUpdateForm(**form)

    # 调用 service 层处理逻辑，返回 UserProfileUpdateResult 实例
    result = update_user_profile(
        user_id=data.id,
        name=data.name,
        intro=data.introduction,
        avatar_file=avatar_file,
        fallback_avatar=data.avatar,
    )

    return Result.success(data=result.dict())


@layout_bp.route('/search-books', methods=['GET'])
def search_books_api():
    # 解析请求参数并验证
    args = SearchBookRequest(**request.args)
    result = search_books(args)
    return Result.success(data=result.dict())
