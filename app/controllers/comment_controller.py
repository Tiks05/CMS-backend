from flask import Blueprint, request

from app.schemas.comment_schema import LikeUpdateRequest, CreateCommentRequest
from app.services.comment_service import get_comments_by_book, increase_likes_by_ids, create_comment
from app.core.response import Result

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/list', methods=['GET'])
def get_comment_list():
    book_id = int(request.args.get('book_id', 0))

    comment_list = get_comments_by_book(book_id)
    return Result.success(comment_list)

@comment_bp.route('/likes', methods=['POST'])
def update_likes():
    data = LikeUpdateRequest(**request.get_json())

    increase_likes_by_ids(data.ids)
    return Result.success()

@comment_bp.route('/create', methods=['POST'])
def create_comment_api():
    data = CreateCommentRequest(**request.json)

    create_comment(data)

    return Result.success()