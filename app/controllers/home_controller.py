from flask import Blueprint, request
from ..core.response import Result
from ..services.home_service import get_top_books_service, get_news_list_service, get_writer_list_service, get_recommend_books, get_adapt_list_service, get_ranking_list
from ..schemas.home_schema import TopBookOut, NewsOut, WriterOut, RecommendResponse, AdaptListResponse

home_bp = Blueprint('home', __name__)

@home_bp.route('/top-books', methods=['GET'])
def get_top_books():
    books = get_top_books_service()

    result = []
    for i, book in enumerate(books):
        # 取 tags 的第一个标签作为 desc
        desc_value = book.tags.split(",")[0] if book.tags else "未知分类"

        cover_url = f"{request.host_url.rstrip('/')}{book.cover_url}" if book.cover_url else ""

        item = {
            "num": f"{i+1:02d}",
            "title": book.title,
            "desc": desc_value,
            "path": f"/bookinfo/{book.id}",
            "pic": cover_url
        }

        result.append(TopBookOut(**item).dict())

    return Result.success(result)

@home_bp.route('/news-list', methods=['GET'])
def get_news_list():
    limit = request.args.get('limit', default=8, type=int)
    news_list = get_news_list_service(limit)

    result = []
    for news in news_list:
        item = {
            "title": news.title,
            "path": f"/newsinfo/{news.id}"
        }
        result.append(NewsOut(**item).dict())

    return Result.success(result)

@home_bp.route('/writer-list', methods=['GET'])
def get_writer_list():
    writers = get_writer_list_service()

    result = []
    for writer in writers:
        item = {
            "title": writer.nickname,
            "desc": f"代表作{writer.masterpiece}" if writer.masterpiece else "",
            "type": writer.author_level,
            "pic": f"{request.host_url.rstrip('/')}{writer.life_photo}" if writer.life_photo else "",
            "path": f"/writerinfo/{writer.id}"
        }
        result.append(WriterOut(**item).dict())

    return Result.success(result)

@home_bp.route('/recommend', methods=['GET'])
def recommend():
    male_result, female_result = get_recommend_books()
    return Result.success(
        RecommendResponse(male=male_result, female=female_result).dict()
    )

@home_bp.route('/adaptlist', methods=['GET'])
def adaptlist():
    limit = request.args.get('limit')
    data = get_adapt_list_service(limit=limit)
    return Result.success(AdaptListResponse(data=data).dict())

@home_bp.route('/ranking', methods=['GET'])
def ranking():
    reader_type = request.args.get('reader_type')  # 男生/女生
    plot_type = request.args.get('plot_type')  # 类别文本

    data = get_ranking_list(reader_type, plot_type)
    return Result.success(data.dict())