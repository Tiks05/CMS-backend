from flask import request
from datetime import datetime
from app.models.book import Book
from app.extensions import db
from sqlalchemy import desc
from app.schemas.library_schema import BookListQuerySchema, BookOutSchema, BookListOutSchema

def get_filtered_books(params: BookListQuerySchema):
    query = db.session.query(Book)

    if params.reader_type:
        query = query.filter(Book.reader_type == params.reader_type)

    if params.category_group and params.category_type:
        key = {
            'theme_type': Book.theme_type,
            'role_type': Book.role_type,
            'plot_type': Book.plot_type
        }.get(params.category_group)
        if key:
            query = query.filter(key == params.category_type)

    if params.status:
        query = query.filter(Book.status == params.status)

    if params.word_count_range:
        if params.word_count_range == '30万以下':
            query = query.filter(Book.word_count < 300000)
        elif params.word_count_range == '30-50万':
            query = query.filter(Book.word_count.between(300000, 500000))
        elif params.word_count_range == '50-100万':
            query = query.filter(Book.word_count.between(500000, 1000000))
        elif params.word_count_range == '100-200万':
            query = query.filter(Book.word_count.between(1000000, 2000000))
        elif params.word_count_range == '200万以上':
            query = query.filter(Book.word_count >= 2000000)

    if params.sort == 'hot':
        query = query.order_by(desc(Book.favorite_count))
    elif params.sort == 'new':
        query = query.order_by(desc(Book.updated_at))
    elif params.sort == 'words':
        query = query.order_by(desc(Book.word_count))

    pagination = query.paginate(page=params.page, per_page=params.pageSize, error_out=False)

    return BookListOutSchema(
        total=pagination.total,
        records=[serialize_book(b) for b in pagination.items]
    ).dict()

def serialize_book(book: Book) -> dict:
    now = datetime.utcnow()
    delta = now - book.updated_at

    if delta.days >= 1:
        time_display = book.updated_at.strftime('%Y-%m-%d %H:%M')
    elif delta.seconds >= 3600:
        hours = delta.seconds // 3600
        time_display = f"{hours}小时前"
    elif delta.seconds >= 60:
        minutes = delta.seconds // 60
        time_display = f"{minutes}分钟前"
    else:
        time_display = f"{delta.seconds}秒前"

    cover_url = f"{request.host_url.rstrip('/')}{book.cover_url}" if book.cover_url else ""

    return BookOutSchema(
        id=book.id,
        title=book.title,
        author=book.author.nickname if book.author else "",
        status=book.status,
        wordCount=book.word_count,
        intro=book.intro,
        coverUrl=cover_url,
        updatedAt=time_display,
        path=f"/bookinfo/{book.id}"
    ).dict()
