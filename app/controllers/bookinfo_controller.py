from flask import Blueprint, request
from ..core.response import Result
from ..services.bookinfo_service import get_book_header, get_book_content, get_chapter_content
from app.schemas.bookinfo_schema import BookHeaderSchema, BookContentSchema

bookinfo_bp = Blueprint('bookinfo', __name__)


@bookinfo_bp.route('/header/<int:book_id>', methods=['GET'])
def book_header(book_id: int):
    result = get_book_header(book_id)

    # 用 Pydantic 模型做数据校验和序列化
    schema = BookHeaderSchema(**result)
    return Result.success(schema.dict())


@bookinfo_bp.route('/content/<int:book_id>', methods=['GET'])
def book_content(book_id: int):
    result = get_book_content(book_id)

    schema = BookContentSchema(**result)
    return Result.success(schema.dict())


@bookinfo_bp.route('/chapter', methods=['GET'])
def get_chapter():
    # 获取并验证参数
    book_id = request.args.get('bookId', type=int)
    volume_id = request.args.get('volumeId', type=int)
    chapter_id = request.args.get('chapterId', type=int)
    # 调用 service 获取章节内容
    data = get_chapter_content(book_id, volume_id, chapter_id)
    return Result.success(data)
