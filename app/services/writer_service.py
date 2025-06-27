from flask import request
from ..models import News, Classroom
from ..schemas.writer_schema import PicNoticeSchema, NoticeSchema, ActiveSchema, ClassroomOutSchema


def get_news_list_by_type(news_type: str, limit: int = 5):
    query = News.query.filter(News.type == news_type).order_by(News.updated_at.desc()).limit(limit)

    if news_type == 'picnotice':
        return [
            PicNoticeSchema(
                cover_url=(
                    f"{request.host_url.rstrip('/')}{item.cover_url}" if item.cover_url else ""
                ),
                title=item.title,
                path=f"/newsinfo/{item.id}",
            ).dict()
            for item in query
        ]

    elif news_type == 'notice':
        return [
            NoticeSchema(title=item.title, path=f"/newsinfo/{item.id}").dict() for item in query
        ]

    elif news_type == 'active':
        return [
            ActiveSchema(
                cover_url=(
                    f"{request.host_url.rstrip('/')}{item.cover_url}" if item.cover_url else ""
                ),
                title=item.title,
                path=f"/newsinfo/{item.id}",
                updated_at=item.updated_at.strftime('%Y-%m-%d'),
            ).dict()
            for item in query
        ]

    return []


def get_classroom_by_category(category_type: str):
    query = Classroom.query

    if category_type:
        query = query.filter(Classroom.category_type == category_type)

    query = query.order_by(Classroom.create_at.desc()).limit(10)

    host = request.host_url.rstrip('/')
    result = []

    for item in query:
        data = ClassroomOutSchema(
            title=item.title,
            intro=item.intro,
            cover_url=f"{request.host_url.rstrip('/')}{item.cover_url}" if item.cover_url else "",
            path=f"/classroom/{item.id}",
            is_include_video=item.is_include_video,
        )
        result.append(data.dict())

    return result
