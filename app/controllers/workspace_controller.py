from flask import Blueprint, request
from ..schemas.workspace_schema import (
    AuthorApplyForm,
    BookCreateForm,
    MyBookListQuery,
    BookUpdateForm,
    ChapterCreateSchema,
    ChapterUpdateSchema,
    LastChapterResponse,
    LatestChapterResponse,
)
from ..services.workspace_service import (
    save_author_application,
    get_author_stats,
    get_notice_list,
    get_news_list,
    get_book_rank_data,
    save_book,
    get_book_list_by_user,
    get_book_detail,
    update_book_info,
    get_last_chapter_info,
    create_chapter,
    get_chapter_list_by_book_id,
    delete_chapter_by_id,
    update_chapter,
    get_chapter_detail_by_id,
    delete_volume_with_chapters,
    update_volume_title,
    create_volume,
    get_last_chapter_by_volume_id,
    get_last_chapter_by_book_id,
    get_latest_chapter_by_book_id,
)
from app.schemas.workspace_schema import BookRankResponse
from ..core.response import Result
from app.core.exceptions import APIException

workspace_bp = Blueprint('workspace', __name__)


@workspace_bp.route('/apply', methods=['POST'])
def author_apply():
    form = request.form
    avatar_file = request.files.get('avatar')  # 上传的新头像（可为空）

    # 使用 Pydantic 解析并校验：id、avatar、name、introduction
    data = AuthorApplyForm(**form)

    # 调用 service 层处理逻辑，返回 AuthorApplyResult 实例
    raw_result = save_author_application(
        user_id=data.id,
        name=data.name,
        intro=data.introduction,
        avatar_file=avatar_file,
        fallback_avatar=data.avatar,
    )

    # 直接 .dict() 返回给前端
    return Result.success(data=raw_result.dict())


@workspace_bp.route('/writer/stats/<int:user_id>', methods=['GET'])
def get_writer_stats(user_id: int):
    data = get_author_stats(user_id)
    return Result.success(data.dict())


@workspace_bp.route('/writer/notice-list', methods=['GET'])
def get_notice_list_route():
    limit = int(request.args.get('limit', 3))
    data = get_notice_list(limit=limit)
    return Result.success([item.dict() for item in data])


@workspace_bp.route('/writer/news-list', methods=['GET'])
def news_list():
    limit = int(request.args.get('limit', 4))
    data = get_news_list(limit=limit)
    return Result.success([item.dict() for item in data])


@workspace_bp.route('/writer/book-rank', methods=['GET'])
def get_book_rank():
    reader_type = request.args.get('type', '')
    category = request.args.get('category', '')

    data = get_book_rank_data(reader_type, category)

    return Result.success(BookRankResponse(**data).dict())


@workspace_bp.route('/writer/create-book', methods=['POST'])
def create_book():
    form = request.form
    cover_file = request.files.get('cover')

    # 校验字段（使用 Pydantic）
    data = BookCreateForm(**form)

    # 保存到数据库
    save_book(data=data, cover_file=cover_file)

    return Result.success('创建成功')


@workspace_bp.route('/writer/my-book-list', methods=['GET'])
def get_my_book_list():
    # Pydantic 校验请求参数
    query = MyBookListQuery(**request.args)

    # 调用 service 获取数据
    data = get_book_list_by_user(user_id=query.user_id)

    return Result.success(data)


@workspace_bp.route('/writer/book-overview/<int:book_id>', methods=['GET'])
def book_overview_detail(book_id: int):
    data = get_book_detail(book_id)
    return Result.success(data.dict())


@workspace_bp.route('/writer/update-book', methods=['POST'])
def update_book():
    form = request.form
    cover_file = request.files.get('cover')

    # 解析并校验字段（可用和 BookCreateForm 类似的 Pydantic 模型）
    data = BookUpdateForm(**form)  # 或创建一个专用的 BookUpdateForm 也行

    # 调用更新逻辑
    update_book_info(data=data, cover_file=cover_file)

    return Result.success('修改成功')


@workspace_bp.route('/writer/get-last-chapterInfo', methods=['GET'])
def get_last_chapter():
    book_id = request.args.get('book_id', type=int)

    data = get_last_chapter_info(book_id)
    return Result.success(data.dict())


@workspace_bp.route('/writer/create-chapter', methods=['POST'])
def post_create_chapter():
    data = ChapterCreateSchema(**request.json)
    create_chapter(data)

    return Result.success()


@workspace_bp.route('/writer/chapter-list', methods=['GET'])
def chapter_list():
    book_id = int(request.args.get('book_id', 0))
    title = request.args.get('title', '').strip()
    volume_id = request.args.get('volume_id', '').strip()
    status = request.args.get('status', '').strip()

    data = get_chapter_list_by_book_id(
        book_id=book_id, title=title, volume_id=volume_id, status=status
    ).dict()
    return Result.success(data)


@workspace_bp.route('/writer/delete-chapter/<int:chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    success = delete_chapter_by_id(chapter_id)
    if not success:
        raise APIException("删除失败", code=40004)
    return Result.success()


@workspace_bp.route('/writer/update-chapter', methods=['POST'])
def update_chapter_view():
    data_dict = request.json
    data = ChapterUpdateSchema(**data_dict)
    update_chapter(data)
    return Result.success()


@workspace_bp.route('/writer/chapter-detail', methods=['GET'])
def chapter_detail():
    book_id = int(request.args.get('book_id', 0))
    chapter_id = int(request.args.get('chapter_id', 0))

    data = get_chapter_detail_by_id(book_id, chapter_id)
    return Result.success(data)


@workspace_bp.route('/writer/delete-volume', methods=['DELETE'])
def delete_volume_api():
    book_id = request.args.get('book_id', type=int)
    volume_id = request.args.get('volume_id', type=int)

    success = delete_volume_with_chapters(book_id, volume_id)
    if not success:
        raise APIException("删除失败", code=40004)
    return Result.success()


@workspace_bp.route('/writer/update-volume', methods=['POST'])
def update_volume_api():
    data = request.get_json()
    volume_id = data.get('id')
    book_id = data.get('book_id')
    title = data.get('title')

    success = update_volume_title(volume_id, book_id, title)
    if success:
        return Result.success()


@workspace_bp.route('/writer/create-volume', methods=['POST'])
def create_volume_api():
    data = request.json
    book_id = data.get('book_id')
    title = data.get('title')
    sort = data.get('sort')

    create_volume(book_id, title, sort)
    return Result.success()


@workspace_bp.get('/writer/last-chapter')
def get_last_chapter_by_book():
    book_id = request.args.get('book_id', type=int)

    data = get_last_chapter_by_book_id(book_id)  # 无数据返回空字典
    return Result.success(LastChapterResponse(**data).dict())


@workspace_bp.get('/writer/last-chapter-by-volume')
def get_last_chapter_by_volume():
    book_id = request.args.get('book_id', type=int)
    volume_id = request.args.get('volume_id', type=int)

    data = get_last_chapter_by_volume_id(book_id, volume_id)

    return Result.success(LastChapterResponse(**data).dict())


@workspace_bp.get('/writer/latest-chapter')
def get_latest_chapter_by_book():
    book_id = request.args.get('book_id', type=int)

    data = get_latest_chapter_by_book_id(book_id)  # 没有章节，返回空字典

    return Result.success(LatestChapterResponse(**data).dict())
