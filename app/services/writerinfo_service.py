import random
from flask import request
from sqlalchemy import func
from app.models.user import User
from app.models.book import Book
from app.models.volume import Volume
from app.models.chapter import Chapter
from app.extensions import db


def get_writer_header_service(writer_id: int):
    user = db.session.query(User).filter_by(id=writer_id, role='author').first()

    # 总字数统计
    total_words = (
        db.session.query(db.func.sum(Book.word_count)).filter_by(user_id=writer_id).scalar() or 0
    )
    # 粉丝数（可按你后续粉丝表统计，这里先写0或模拟）
    follower_count = random.randint(30000, 150000)

    return {
        "nickname": user.nickname,
        "avatar_url": f"{request.host_url.rstrip('/')}{user.avatar}" if user.avatar else "",
        "signature": user.signature,
        "intro": user.signature,  # 你有 intro 字段就用 intro
        "become_author_at": user.become_author_at.isoformat() if user.become_author_at else "",
        "total_words": total_words,
        "follower_count": follower_count,
        # 其他字段可补充
    }


def get_writer_works_service(writer_id: int):
    books = db.session.query(Book).filter_by(user_id=writer_id).all()
    works = []

    for book in books:
        # 最大章节号
        max_chapter_num = (
            db.session.query(func.max(Chapter.chapter_num))
            .join(Volume, Volume.id == Chapter.volume_id)
            .filter(Volume.book_id == book.id)
            .scalar()
        ) or 0

        # 最大章节标题
        max_chapter_title = None
        if max_chapter_num:
            max_chapter = (
                db.session.query(Chapter)
                .join(Volume, Volume.id == Chapter.volume_id)
                .filter(Volume.book_id == book.id, Chapter.chapter_num == max_chapter_num)
                .first()
            )
            if max_chapter:
                max_chapter_title = max_chapter.title

        # 总字数（动态统计章节 word_count）
        total_word_count = (
            db.session.query(func.sum(Chapter.word_count))
            .join(Volume, Volume.id == Chapter.volume_id)
            .filter(Volume.book_id == book.id)
            .scalar()
        ) or 0

        works.append(
            {
                "title": book.title,
                "cover_url": (
                    f"{request.host_url.rstrip('/')}{book.cover_url}" if book.cover_url else ""
                ),
                "status": book.status,
                "word_count": total_word_count,
                "tags": book.tags,
                "intro": book.intro,
                "updated_at": book.updated_at.isoformat() if book.updated_at else "",
                "bookinfo_path": f"/bookinfo/{book.id}",
                "max_chapter": max_chapter_num,
                "max_chapter_title": max_chapter_title,
            }
        )

    return works
