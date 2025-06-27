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

    # 获取最新章节（根据更新时间排序）
    latest_chapter = (
        db.session.query(Chapter)
        .join(Volume, Volume.id == Chapter.volume_id)
        .filter(Volume.book_id == book_id)
        .order_by(Chapter.updated_at.desc())
        .first()
    )

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
            'cover_url': (
                f"{request.host_url.rstrip('/')}{book.cover_url}" if book.cover_url else ''
            ),
            'status': book.status or '',
            'word_count': total_word_count,
            'tags': book.tags or '',
            'updated_at': book.updated_at.strftime('%Y-%m-%d %H:%M:%S') if book.updated_at else '',
            'latest_chapter': latest_chapter.chapter_num if latest_chapter else 0,
            'latest_chapter_title': latest_chapter.title if latest_chapter else '',
        },
        'author': {
            'nickname': author.nickname if author else '',
            'cover_url': (
                f"{request.host_url.rstrip('/')}{author.avatar}" if author and author.avatar else ''
            ),
            'signature': author.signature if author else '',
            'path': f'/writerinfo/{author.id}' if author else '',
        },
    }


def get_book_content(book_id: int) -> dict:

    def num_to_chinese(num: int) -> str:
        digits = '零一二三四五六七八九'
        if num <= 10:
            return '十' if num == 10 else digits[num]
        elif num < 20:
            return '十' + digits[num % 10]
        else:
            tens = num // 10
            ones = num % 10
            return digits[tens] + '十' + (digits[ones] if ones > 0 else '')

    volumes = (
        db.session.query(Volume).filter(Volume.book_id == book_id).order_by(Volume.sort.asc()).all()
    )

    result = []
    for idx, vol in enumerate(volumes, start=1):
        chapters = sorted(vol.chapters, key=lambda c: c.chapter_num)
        chapter_list = [
            {'title': chap.title, 'path': f'/read/{book_id}/{vol.sort}/{chap.chapter_num}'}
            for chap in chapters
        ]

        chinese_idx = num_to_chinese(idx)
        result.append(
            {
                'title': f'第{chinese_idx}卷：{vol.title}',
                'chapter_count': len(chapter_list),
                'chapters': chapter_list,
            }
        )

    book = db.session.query(Book).filter(Book.id == book_id).first()
    intro = book.intro if book else ''

    return {'intro': intro, 'volumes': result}


def get_chapter_content(book_id: int, volume_sort: int, chapter_num: int) -> Dict:
    # 1. 通过 book_id + volume.sort 查对应 Volume
    volume = (
        db.session.query(Volume)
        .filter(Volume.book_id == book_id, Volume.sort == volume_sort)
        .first()
    )
    if not volume:
        raise ValueError("该分卷不存在或不属于当前书籍")

    # 2. 通过 volume.id + chapter_num 查找 Chapter
    chapter = (
        db.session.query(Chapter)
        .filter(Chapter.volume_id == volume.id, Chapter.chapter_num == chapter_num)
        .first()
    )
    if not chapter:
        raise ValueError("章节不存在或不属于该分卷")

    # 3. 获取书名（防止为空）
    book_title = volume.book.title if volume.book else ""

    # 4. 获取上一章
    prev_chapter = (
        db.session.query(Chapter)
        .filter(Chapter.volume_id == volume.id, Chapter.chapter_num < chapter.chapter_num)
        .order_by(Chapter.chapter_num.desc())
        .first()
    )

    # 5. 获取下一章
    next_chapter = (
        db.session.query(Chapter)
        .filter(Chapter.volume_id == volume.id, Chapter.chapter_num > chapter.chapter_num)
        .order_by(Chapter.chapter_num.asc())
        .first()
    )

    # 6. 组织响应结构
    return ChapterReadResponse(
        book_title=book_title,
        chapter_title=chapter.title,
        word_count=chapter.word_count or len(chapter.content or ""),
        updated_at=chapter.updated_at.strftime('%Y-%m-%d') if chapter.updated_at else "",
        content=chapter.content or "",
        chapter_index=chapter.chapter_num or 1,
        prev_chapter_id=prev_chapter.chapter_num if prev_chapter else None,
        next_chapter_id=next_chapter.chapter_num if next_chapter else None,
    ).dict()
