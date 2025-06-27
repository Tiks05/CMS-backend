from flask import Blueprint, request
from app.services.writer_service import get_news_list_by_type, get_classroom_by_category
from app.core.response import Result

writer_bp = Blueprint('writer', __name__)


@writer_bp.route('/news', methods=['GET'])
def get_news_list():
    news_type = request.args.get('type', 'normal')
    limit = int(request.args.get('limit', 5))

    if news_type != 'notice':
        news_type = 'active'

    data = get_news_list_by_type(news_type=news_type, limit=limit)
    return Result.success(data)


@writer_bp.route('/classroom', methods=['GET'])
def get_classroom_list():
    category_type = request.args.get('category_type', '').strip()

    data = get_classroom_by_category(category_type=category_type)
    return Result.success(data)
