from sqlalchemy.orm import selectinload
from ..models import Book, News, User
from ..schemas.home_schema import RankingBookOut, BookRankingOut, BookOut, AdaptBookOut
from app.extensions import db
from flask import request
import random

def get_top_books_service():
    # 取前 30 本书，按收藏数降序排序（你后续可以换成综合评分、人气等等）
    books = Book.query.order_by(Book.favorite_count.desc()).limit(30).all()
    return books

def get_news_list_service(limit):
    news_list = News.query.order_by(News.created_at.desc()).limit(limit).all()
    return news_list

def get_writer_list_service():
    palace_writers = User.query.filter(User.author_level == '殿堂作家').all()

    golden_writers = User.query.filter(User.author_level == '金番作家').all()

    # 拼接在一起，殿堂作家在前，金番作家在后
    writers = palace_writers + golden_writers

    return writers

def get_recommend_books():
    def query_books(reader_type):
        return Book.query.options(selectinload(Book.author)) \
            .filter(Book.reader_type == reader_type) \
            .all()

    def convert(books):
        return [
            BookOut(
                id=book.id,
                title=book.title,
                desc=book.intro or "",
                cover_url=f"{request.host_url.rstrip('/')}{book.cover_url}" if book.cover_url else "",
                author_nickname=book.author.nickname if book.author else "",
                path=f"/bookinfo/{book.id}"
            )
            for book in books
        ]

    male_books = query_books('男生')
    female_books = query_books('女生')

    return (
        convert(random.sample(male_books, min(5, len(male_books)))),
        convert(random.sample(female_books, min(5, len(female_books))))
    )

def get_adapt_list_service(limit):
    books = db.session.query(Book).options(selectinload(Book.author)).limit(limit).all()

    return [
        AdaptBookOut(
            id=book.id,
            pic=f"{request.host_url.rstrip('/')}{book.cover_url}" if book.cover_url else "",
            path=f"/bookinfo/{book.id}"
        )
        for book in books
    ]

def get_ranking_list(reader_type: str, plot_type: str) -> BookRankingOut:
    query = db.session.query(Book).filter(Book.reader_type == reader_type)
    query = query.filter(Book.plot_type == plot_type)

    read_books = query.order_by(Book.favorite_count.desc()).limit(10).all()
    new_books = query.order_by(Book.created_at.desc()).limit(10).all()

    def convert(books):
        return [
            RankingBookOut(
                num=str(i + 1).zfill(2),
                title=book.title,
                desc=(book.intro[:35] + '...') if book.intro else "",
                path=f"/bookinfo/{book.id}",
                pic=f"{request.host_url.rstrip('/')}{book.cover_url}" if book.cover_url else "",
                author=book.author.nickname if book.author else ""
            )
            for i, book in enumerate(books)
        ]

    return BookRankingOut(
        plot_type=plot_type,
        child=convert(read_books),
        new_child=convert(new_books)
    )