from typing import Dict
from flask import request
from sqlalchemy import func
from app.extensions import db
from app.models.book import Book
from app.models.volume import Volume
from app.models.chapter import Chapter
from app.schemas.bookinfo_schema import ChapterReadResponse

def get_book_header(book_id: int) -> dict:
    book = db.session.query(Book).filter(Book.id == book_id).first()
    if not book:
        return {}

    # 最大章节号（跨 volume）
    max_chapter = (
        db.session.query(func.max(Chapter.chapter_num))
        .join(Volume, Volume.id == Chapter.volume_id)
        .filter(Volume.book_id == book_id)
        .scalar()
    ) or 0

    total_word_count = (
                           db.session.query(func.sum(Chapter.word_count))
                           .join(Volume, Volume.id == Chapter.volume_id)
                           .filter(Volume.book_id == book_id)
                           .scalar()
                       ) or 0

    author = book.author

    return {
        'book': {
            'id': book.id,
            'title': book.title or '',
            'cover_url': f"{request.host_url.rstrip('/')}{book.cover_url}" if book.cover_url else '',
            'status': book.status or '',
            'word_count': total_word_count or 0,
            'tags': book.tags or '',
            'updated_at': book.updated_at.strftime('%Y-%m-%d %H:%M:%S') if book.updated_at else '',
            'max_chapter': max_chapter
        },
        'author': {
            'nickname': author.nickname if author else '',
            'cover_url': f"{request.host_url.rstrip('/')}{author.avatar}" if author and author.avatar else '',
            'signature': author.signature if author else '',
            'path': f'/writerinfo/{author.id}' if author else ''
        }
    }

def get_book_content(book_id: int) -> dict:
    volumes = (
        db.session.query(Volume)
        .filter(Volume.book_id == book_id)
        .order_by(Volume.sort.asc())
        .all()
    )

    result = []
    for vol in volumes:
        chapters = sorted(vol.chapters, key=lambda c: c.chapter_num)
        chapter_list = [{
            'title': chap.title,
            'path': f'/read/{book_id}/{vol.sort}/{chap.chapter_num}'
        } for chap in chapters]

        result.append({
            'title': vol.title,
            'chapter_count': len(chapter_list),
            'chapters': chapter_list
        })

    book = db.session.query(Book).filter(Book.id == book_id).first()
    intro = book.intro if book else ''

    return {
        'intro': intro,
        'volumes': result
    }

def get_chapter_content(book_id: int, volume_id: int, chapter_id: int) -> Dict:
    # 1. 用 volume.sort 和 book_id 查出对应的 volume 对象
    volume = db.session.query(Volume).filter(
        Volume.sort == volume_id,  # 注意这里传入的是 sort，不是 volume 表主键 id
        Volume.book_id == book_id
    ).first()
    if not volume:
        raise ValueError("该分卷不属于当前书籍")

    # 2. 查找章节，确保 chapter_num 属于该 volume
    chapter = (
        db.session.query(Chapter)
        .filter(Chapter.chapter_num == chapter_id, Chapter.volume_id == volume.id)
        .first()
    )
    if not chapter:
        raise ValueError("章节不存在或不属于该分卷")

    # 3. 获取书名（防止 book 关系为空）
    book_title = volume.book.title if volume.book else ""

    # 4. 上一章（注意用 volume.id）
    prev_chapter = (
        db.session.query(Chapter)
        .filter(Chapter.volume_id == volume.id, Chapter.chapter_num < chapter.chapter_num)
        .order_by(Chapter.chapter_num.desc())
        .first()
    )

    # 5. 下一章
    next_chapter = (
        db.session.query(Chapter)
        .filter(Chapter.volume_id == volume.id, Chapter.chapter_num > chapter.chapter_num)
        .order_by(Chapter.chapter_num.asc())
        .first()
    )

    # 6. 返回数据结构化结果
    return ChapterReadResponse(
        book_title=book_title,
        chapter_title=chapter.title,
        word_count=chapter.word_count or len(chapter.content or ""),
        updated_at=chapter.updated_at.strftime('%Y-%m-%d') if chapter.updated_at else "",
        content=chapter.content or "",
        chapter_index=chapter.chapter_num or 1,
        prev_chapter_id=prev_chapter.id if prev_chapter else None,
        next_chapter_id=next_chapter.id if next_chapter else None
    ).dict()