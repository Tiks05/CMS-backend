from datetime import datetime
from flask import request
import random
from werkzeug.datastructures import FileStorage
from app.core.exceptions import APIException
from app.models import Chapter, Volume
from app.models.user import User
from app.models.book import Book
from app.models.news import News
from app.extensions import db
from app.schemas.workspace_schema import (
    AuthorApplyResult,
    AuthorStatsSchema,
    NoticeItemSchema,
    NewsListItemSchema,
    SortItem,
    BookDetailSchema,
    ChapterInfoSchema,
    ChapterCreateSchema,
    VolumeItem,
    ChapterListResponse,
    ChapterItem,
    ChapterUpdateSchema,
    ChapterDetailSchema,
)
from app.utils.image_utils import save_uploaded_image
from typing import Dict, Any


def save_author_application(
    user_id: int, name: str, intro: str, avatar_file: FileStorage = None, fallback_avatar: str = ''
) -> AuthorApplyResult:
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
    user.role = 'author'
    user.author_level = '签约作家'
    user.become_author_at = datetime.utcnow().isoformat()
    db.session.commit()

    # 3. 返回结构化数据（绝对路径给前端）
    return AuthorApplyResult(
        avatar=avatar_url,
        nickname=user.nickname,
        become_author_at=str(user.become_author_at),
        signature=user.signature,
    )


def get_author_stats(writer_id: int) -> AuthorStatsSchema:
    total_words = (
        db.session.query(db.func.sum(Book.word_count)).filter_by(user_id=writer_id).scalar() or 0
    )
    follower_count = random.randint(30000, 150000)

    return AuthorStatsSchema(fans_count=follower_count, total_words=total_words)


def get_notice_list(limit: int = 3) -> list[NoticeItemSchema]:
    records = (
        News.query.filter_by(type='active', is_notice=True)
        .order_by(News.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        NoticeItemSchema(
            notice_url=(
                f"{request.host_url.rstrip('/')}{item.notice_url}" if item.notice_url else ""
            ),
            title=item.title,
            time=item.updated_at.strftime('%m.%d - 10.03'),  # 示例
            path=f"/newsinfo/{item.id}",
        )
        for item in records
    ]


def get_news_list(limit: int = 4) -> list[NewsListItemSchema]:
    records = (
        News.query.filter_by(type='active').order_by(News.created_at.desc()).limit(limit).all()
    )

    return [NewsListItemSchema(title=item.title, path=f"/newsinfo/{item.id}") for item in records]


def get_book_rank_data(reader_type: str, category: str) -> Dict[str, Any]:
    books = (
        db.session.query(Book)
        .filter(Book.reader_type == reader_type)
        .filter(Book.plot_type == category)
        .filter(Book.status == '连载中')  # 仅展示连载中的
        .order_by(Book.created_at.desc())
        .limit(4)
        .all()
    )

    # 构建榜单项目列表
    child_list: list[SortItem] = []
    for index, book in enumerate(books):
        item = SortItem(
            num=index + 1,
            title=book.title,
            path=f"/bookinfo/{book.id}",
            pic=f"{request.host_url.rstrip('/')}{book.cover_url}" if book.cover_url else "",
            author=book.author.nickname if book.author and book.author.nickname else "",
            desc=book.intro or "",
        )
        child_list.append(item)

    return {"plot_type": category, "child": child_list}


def save_book(data, cover_file: FileStorage = None):
    # 1. 封面上传处理
    if cover_file:
        relative_path, absolute_url = save_uploaded_image(file=cover_file, sub_folder='/covers')
        cover_url = relative_path
    else:
        cover_url = '/static/uploads/covers/default_cover.png'  # 使用默认封面或空字符串

    # 2. 构造主角字段（合并 hero1 + hero2）
    hero = ' / '.join(filter(None, [data.hero1.strip(), data.hero2.strip()]))

    # 3. 创建 Book 实例
    book = Book(
        user_id=data.id,
        title=data.name.strip(),
        reader_type=data.reader_type,
        tags=data.tag.strip(),
        intro=data.introduction.strip()
        or "新作品出炉，欢迎大家前往番茄小说阅读我的作品，希望大家能够喜欢，你们的关注是我写作的动力，我会努力讲好每个故事！",
        hero=hero,
        cover_url=cover_url,
        status='连载中',  # 默认状态
        word_count=0,  # 初始字数为 0
        word_count_range='30万以下',  # 默认范围
    )

    # 4. 写入数据库
    db.session.add(book)
    db.session.commit()


def get_book_list_by_user(user_id: int) -> list[dict]:
    books = db.session.query(Book).filter_by(user_id=user_id).all()
    result = []

    for book in books:
        # 1. 获取该书所有 volume_id
        volume_ids = db.session.query(Volume.id).filter_by(book_id=book.id).all()
        volume_ids = [v.id for v in volume_ids]

        # 2. 获取最近章节（按时间倒序）
        recent_chapter = (
            db.session.query(Chapter)
            .filter(Chapter.volume_id.in_(volume_ids))
            .order_by(Chapter.created_at.desc())
            .first()
        )

        # 3. 统计章节数量与总字数
        chapter_count = db.session.query(Chapter).filter(Chapter.volume_id.in_(volume_ids)).count()
        word_total = (
            db.session.query(db.func.sum(Chapter.word_count))
            .filter(Chapter.volume_id.in_(volume_ids))
            .scalar()
        ) or 0

        result.append(
            {
                "id": book.id,
                "title": book.title,
                "pic": (
                    f"{request.host_url.rstrip('/')}{book.cover_url}"
                    if book.cover_url
                    else "/src/assets/images/workspace/writer/default_cover.png"
                ),
                "latestChapterTitle": recent_chapter.title if recent_chapter else "暂无章节",
                "latestChapterNum": recent_chapter.chapter_num if recent_chapter else 0,
                "totalChapters": chapter_count,
                "words": word_total,
                "status": book.status or "连载中",
                "path": f"/bookinfo/{book.id}",
            }
        )

    return result


def get_book_detail(book_id: int) -> BookDetailSchema:
    book = db.session.query(Book).filter(Book.id == book_id).first()

    return BookDetailSchema(
        id=book.id,
        title=book.title,
        cover_url=f"{request.host_url.rstrip('/')}{book.cover_url}",
        target_readers=book.reader_type or "-",
        tags=book.tags or "-",
        main_roles=book.hero or "-",
        intro=book.intro or "",
        created_at=book.created_at.strftime("%Y-%m-%d %H:%M"),
        status="正常",  # 可换成具体检查结果
        contract_status=book.sign_status or "未签约",
        update_status=book.status or "连载中",
    )


def delete_book_by_id(book_id: int):
    book = db.session.get(Book, book_id)

    # 查找该书所有 volume_id
    volume_ids = db.session.query(Volume.id).filter(Volume.book_id == book_id).all()
    volume_ids = [vid for (vid,) in volume_ids]  # 解包为纯 ID 列表

    # 删除章节（根据 volume_id）
    if volume_ids:
        db.session.query(Chapter).filter(Chapter.volume_id.in_(volume_ids)).delete(
            synchronize_session=False
        )

    # 删除分卷
    db.session.query(Volume).filter(Volume.book_id == book_id).delete(synchronize_session=False)

    # 删除书籍
    db.session.delete(book)

    db.session.commit()


def update_book_info(data, cover_file: FileStorage = None):
    # 1. 查找原书籍
    book = db.session.query(Book).filter(Book.id == data.book_id).first()

    # 2. 封面上传（如有则替换）
    if cover_file:
        relative_path, _ = save_uploaded_image(file=cover_file, sub_folder='/covers')
        book.cover_url = relative_path

    # 3. 主角名合并
    book.hero = data.hero.strip()

    # 4. 其他字段更新
    book.title = data.name.strip()
    book.reader_type = data.reader_type
    book.tags = data.tag.strip()
    book.intro = data.introduction.strip()

    # 5. 提交修改
    db.session.commit()


def get_last_chapter_info(book_id: int) -> ChapterInfoSchema:
    """
    查询某本书的最新一章（通过卷表间接查章节）
    """
    # Step 1: 查询该书所有卷的 ID
    volume_ids = db.session.query(Volume.id).filter(Volume.book_id == book_id).subquery()

    # Step 2: 查这些卷里最新的一章（按卷排序 + 章序号排序）
    chapter = (
        db.session.query(Chapter)
        .filter(Chapter.volume_id.in_(volume_ids))
        .join(Volume, Chapter.volume_id == Volume.id)
        .order_by(Volume.sort.desc(), Chapter.chapter_num.desc())
        .first()
    )

    if not chapter:
        return ChapterInfoSchema()

    # Step 3: 获取该章所在卷的标题与排序
    volume = chapter.volume  # 因为有 relationship，可直接拿

    return ChapterInfoSchema(
        volume_index=volume.sort,
        volume_title=volume.title,
        chapter_index=chapter.chapter_num,
        chapter_title=chapter.title,
    )


def create_chapter(data: ChapterCreateSchema) -> None:
    if data.volume_id:
        # 有 volume_id：查找该卷
        volume = db.session.query(Volume).filter(Volume.id == data.volume_id).first()
        if not volume:
            raise ValueError("指定的分卷不存在")

    else:
        # 无 volume_id：查 book 的最后一卷
        volume = (
            db.session.query(Volume)
            .filter(Volume.book_id == data.book_id)
            .order_by(Volume.sort.desc())
            .first()
        )

        if not volume:
            # 若该书没有任何分卷，则新建“第一卷”
            volume = Volume(book_id=data.book_id, title='第一卷', sort=1)
            db.session.add(volume)
            db.session.flush()  # 获取 volume.id

    # 获取该卷下最后一个章节编号
    last_chapter = (
        db.session.query(Chapter)
        .filter(Chapter.volume_id == volume.id)
        .order_by(Chapter.chapter_num.desc())
        .first()
    )
    next_chapter_num = (last_chapter.chapter_num if last_chapter else 0) + 1

    # 创建新章节
    new_chapter = Chapter(
        volume_id=volume.id,
        chapter_num=next_chapter_num,
        title=data.title,
        content=data.content,
        word_count=data.word_count,
    )

    db.session.add(new_chapter)
    db.session.commit()


status_mapping = {
    'published': '已发布',
    'reviewing': '审核中',
    'rejected': '审核不通过',
    'pending': '待发布',
}


def get_chapter_list_by_book_id(
    book_id: int, title: str = '', volume_id: str = '', status: str = ''
) -> ChapterListResponse:
    # 获取书籍
    book = db.session.query(Book).filter(Book.id == book_id).first()

    # 获取分卷
    volumes = db.session.query(Volume).filter(Volume.book_id == book_id).order_by(Volume.sort).all()

    volume_items = [
        VolumeItem(
            id=v.id,
            book_id=v.book_id,
            title=v.title,
            sort=v.sort or 0,
            created_at=v.created_at.strftime('%Y-%m-%d %H:%M'),
        )
        for v in volumes
    ]

    # 查询章节（通过 Volume 关联 Book）
    query = db.session.query(Chapter).join(Volume).filter(Volume.book_id == book_id)

    if title:
        query = query.filter(Chapter.title.ilike(f"%{title}%"))
    if volume_id:
        query = query.filter(Chapter.volume_id == int(volume_id))
    if status:
        query = query.filter(Chapter.status == status)

    chapters = query.order_by(Chapter.chapter_num).all()

    chapter_items = [
        ChapterItem(
            id=c.id,
            volume_id=c.volume_id,
            chapter_num=c.chapter_num,
            title=c.title,
            word_count=c.word_count or len(c.content or ''),
            updated_at=c.updated_at.strftime('%Y-%m-%d %H:%M'),
            status=c.status,
            status_text=status_mapping.get(c.status, '未知状态'),
            typo_count=0,
        )
        for c in chapters
    ]

    return ChapterListResponse(title=book.title, volumes=volume_items, list=chapter_items)


def delete_chapter_by_id(chapter_id: int) -> bool:
    """根据章节 ID 删除章节"""
    chapter = db.session.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise ValueError("章节不存在")

    db.session.delete(chapter)
    db.session.commit()
    return True


def update_chapter(data: ChapterUpdateSchema) -> None:
    # 查询章节
    chapter = db.session.query(Chapter).filter(Chapter.id == data.chapter_id).first()
    if not chapter:
        raise APIException("章节不存在", code=40404)

    # 检查该章节是否属于对应书籍的 volume
    volume = db.session.query(Volume).filter(Volume.id == chapter.volume_id).first()
    if not volume or volume.book_id != data.book_id:
        raise APIException("章节不属于该书籍", code=40303)

    # 更新字段
    chapter.chapter_num = data.chapter_num
    chapter.title = data.title
    chapter.content = data.content
    chapter.word_count = data.word_count

    db.session.commit()


def get_chapter_detail_by_id(book_id: int, chapter_id: int) -> dict:
    chapter = db.session.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise APIException("章节不存在", code=40404)

    volume = db.session.query(Volume).filter(Volume.id == chapter.volume_id).first()
    if not volume or volume.book_id != book_id:
        raise APIException("章节不属于该书籍", code=40303)

    return ChapterDetailSchema(
        volume_index=volume.sort,
        volume_title=volume.title,
        chapter_num=chapter.chapter_num,
        title=chapter.title,
        content=chapter.content,
    ).dict()


def delete_volume_with_chapters(book_id: int, volume_id: int):
    # 查询目标分卷是否存在，并确保属于该书籍
    volume = (
        db.session.query(Volume).filter(Volume.id == volume_id, Volume.book_id == book_id).first()
    )
    if not volume:
        return False

    # 删除该分卷下所有章节
    db.session.query(Chapter).filter(Chapter.volume_id == volume_id).delete()

    # 删除分卷
    db.session.delete(volume)

    # 提交事务
    db.session.commit()
    return True


def update_volume_title(volume_id: int, book_id: int, new_title: str) -> bool:
    # 查询是否存在该分卷且属于该书籍
    volume = db.session.query(Volume).filter_by(id=volume_id, book_id=book_id).first()
    if not volume:
        return False

    # 修改标题
    volume.title = new_title

    # 提交修改
    db.session.commit()
    return True


def create_volume(book_id: int, title: str, sort: int):
    new_volume = Volume(book_id=book_id, title=title, sort=sort)
    db.session.add(new_volume)
    db.session.commit()
    return new_volume.id


def get_last_chapter_by_book_id(book_id: int):
    # 获取该书的最后一卷（按 sort 倒序）
    last_volume = (
        db.session.query(Volume)
        .filter(Volume.book_id == book_id)
        .order_by(Volume.sort.desc())
        .first()
    )
    if not last_volume:
        return None

    # 获取该卷最后一章
    last_chapter = (
        db.session.query(Chapter)
        .filter(Chapter.volume_id == last_volume.id)
        .order_by(Chapter.chapter_num.desc())
        .first()
    )

    return {
        "last_volume_id": last_volume.sort,
        "last_volume_title": last_volume.title,
        "chapter_index": last_chapter.chapter_num if last_chapter else 0,
        "chapter_title": last_chapter.title if last_chapter else "",
        "updated_at": last_chapter.updated_at.strftime("%Y-%m-%d %H:%M:%S") if last_chapter else "",
    }


def get_last_chapter_by_volume_id(book_id: int, volume_id: int):
    current_volume = (
        db.session.query(Volume).filter(Volume.id == volume_id, Volume.book_id == book_id).first()
    )
    if not current_volume:
        return None

    # 所有分卷中 sort 最大的那一卷（即最后一卷）
    last_volume = (
        db.session.query(Volume)
        .filter(Volume.book_id == book_id)
        .order_by(Volume.sort.desc())
        .first()
    )

    # 最后一卷的最后一章
    last_chapter = (
        db.session.query(Chapter)
        .filter(Chapter.volume_id == last_volume.id)
        .order_by(Chapter.chapter_num.desc())
        .first()
    )

    return {
        "volume_title": current_volume.title,  # 当前写入卷
        "current_volume_id": current_volume.sort,
        "last_volume_id": last_volume.sort,
        "last_volume_title": last_volume.title,
        "chapter_index": last_chapter.chapter_num if last_chapter else 0,
        "chapter_title": last_chapter.title if last_chapter else "",
        "updated_at": last_chapter.updated_at.strftime("%Y-%m-%d %H:%M:%S") if last_chapter else "",
    }


def get_latest_chapter_by_book_id(book_id: int):

    # 从 Volume 表筛选出该书的所有分卷，并连接其下的章节
    result = (
        db.session.query(Chapter, Volume)
        .join(Volume, Chapter.volume_id == Volume.id)
        .filter(Volume.book_id == book_id)
        .order_by(Chapter.updated_at.desc())
        .first()
    )

    if not result:
        return None  # 没有任何章节

    chapter, volume = result

    return {
        "latest_volume_sort": volume.sort,
        "latest_chapter_num": chapter.chapter_num,
        "latest_chapter_title": chapter.title,
        "latest_chapter_updated_at": chapter.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
