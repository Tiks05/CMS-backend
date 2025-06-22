from flask import request
from app.models.news import News
from app.extensions import db
from app.schemas.module_schema import BannerItem  # 引入 Pydantic schema

def get_banner_list(limit: int):
    records = (
        db.session.query(News.id, News.banner_url)
        .filter(News.is_banner == True, News.type == 'active')
        .order_by(News.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        BannerItem(
            banner_url=f"{request.host_url.rstrip('/')}{banner_url}" if banner_url else "",
            path=f"/classroom/{news_id}"
        ).dict()
        for news_id, banner_url in records
    ]
