from datetime import timedelta, datetime

from flask import request
from sqlalchemy import desc, or_, and_, func
from werkzeug.datastructures import FileStorage

from app.models import Volume, Chapter, Book
from app.models.user import User
from app.extensions import db
from app.schemas.layout_schema import (
    UserProfileUpdateResult,
    SearchBookResponse,
    SearchBookItem,
    SearchBookRequest,
)
from app.utils.image_utils import save_uploaded_image


def update_user_profile(
    user_id: int, name: str, intro: str, avatar_file: FileStorage = None, fallback_avatar: str = ''
) -> UserProfileUpdateResult:
    # 1. 头像上传处理
    if avatar_file:
        relative_path, avatar_url = save_uploaded_image(file=avatar_file, sub_folder='user/avatars')
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
        avatar=avatar_url, nickname=user.nickname, signature=user.signature
    )


def search_books(data: SearchBookRequest) -> SearchBookResponse:
    query = db.session.query(Book, User.nickname).join(User, Book.user_id == User.id)

    # 模糊搜索
    if data.keyword:
        query = query.filter(
            or_(Book.title.ilike(f"%{data.keyword}%"), User.nickname.ilike(f"%{data.keyword}%"))
        )

    # 连载状态筛选
    if data.stateindex == 1:
        query = query.filter(Book.status == "已完结")
    elif data.stateindex == 2:
        query = query.filter(Book.status == "连载中")

    # 字数筛选
    if data.numindex == 1:
        query = query.filter(Book.word_count < 300000)
    elif data.numindex == 2:
        query = query.filter(Book.word_count.between(300000, 500000))
    elif data.numindex == 3:
        query = query.filter(Book.word_count.between(500000, 1000000))
    elif data.numindex == 4:
        query = query.filter(Book.word_count > 1000000)

    # 更新时间筛选
    now = datetime.now()
    if data.timeindex == 1:
        query = query.filter(Book.updated_at >= now - timedelta(minutes=30))
    elif data.timeindex == 2:
        today = datetime(now.year, now.month, now.day)
        query = query.filter(Book.updated_at >= today)
    elif data.timeindex == 3:
        monday = datetime(now.year, now.month, now.day) - timedelta(days=now.weekday())
        query = query.filter(Book.updated_at >= monday)
    elif data.timeindex == 4:
        first_day = datetime(now.year, now.month, 1)
        query = query.filter(Book.updated_at >= first_day)
    elif data.timeindex == 5:
        jan1 = datetime(now.year, 1, 1)
        query = query.filter(Book.updated_at >= jan1)

    # 排序
    if data.type == 1:
        query = query.order_by(desc(Book.favorite_count))
    elif data.type == 2:
        query = query.order_by(desc(Book.updated_at))
    else:
        query = query.order_by(desc(Book.id))

    total = query.count()
    books = query.offset((data.page - 1) * data.pageSize).limit(data.pageSize).all()
    book_ids = [b.id for b, _ in books]

    # 第一章路径映射
    first_chapters = (
        db.session.query(Volume.book_id, Volume.sort.label("volume_sort"), Chapter.chapter_num)
        .join(Chapter, Volume.id == Chapter.volume_id)
        .filter(Volume.book_id.in_(book_ids), Chapter.status == "published")
        .order_by(Volume.book_id.asc(), Volume.sort.asc(), Chapter.chapter_num.asc())
        .all()
    )

    path_map = {}
    for row in first_chapters:
        if row.book_id not in path_map:
            path_map[row.book_id] = f"/read/{row.book_id}/{row.volume_sort}/{row.chapter_num}"

    # 最新章节标题 + 路径
    latest_time_subq = (
        db.session.query(
            Volume.book_id.label("book_id"), func.max(Chapter.created_at).label("latest_time")
        )
        .join(Chapter, Volume.id == Chapter.volume_id)
        .filter(Volume.book_id.in_(book_ids), Chapter.status == "published")
        .group_by(Volume.book_id)
        .subquery()
    )

    latest_chapters = (
        db.session.query(
            Volume.book_id, Chapter.title, Volume.sort.label("volume_sort"), Chapter.chapter_num
        )
        .join(Chapter, Volume.id == Chapter.volume_id)
        .join(
            latest_time_subq,
            and_(
                Volume.book_id == latest_time_subq.c.book_id,
                Chapter.created_at == latest_time_subq.c.latest_time,
            ),
        )
        .all()
    )

    update_map = {
        book_id: {"title": title, "path": f"/read/{book_id}/{volume_sort}/{chapter_num}"}
        for book_id, title, volume_sort, chapter_num in latest_chapters
    }

    # 构造响应数据
    records = []
    for book, nickname in books:
        update_info = update_map.get(book.id, {})
        item = SearchBookItem(
            title=book.title,
            author=nickname,
            status=book.status or "",
            wordCount=book.word_count or 0,
            intro=book.intro or "",
            updatedAt=book.updated_at.strftime('%Y-%m-%d %H:%M'),
            pic=request.host_url.rstrip('/')
            + (book.cover_url or '/static/uploads/covers/default.png'),
            people=book.favorite_count,
            update=update_info.get("title", "暂无更新"),
            path=f"/bookinfo/{book.id}",
            readPath=path_map.get(book.id, f"/read/{book.id}/1/1"),
            updatePath=update_info.get("path", f"/read/{book.id}/1/1"),  # 默认跳转
        )
        records.append(item)

    return SearchBookResponse(total=total, records=records)
