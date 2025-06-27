from sqlalchemy import String, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.extensions import db


class News(db.Model):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment='资讯标题')
    content: Mapped[str] = mapped_column(Text, nullable=True, comment='资讯内容')
    notice_url: Mapped[str] = mapped_column(String(255), nullable=True, comment='资讯图路径')
    cover_url: Mapped[str] = mapped_column(String(255), nullable=True, comment='封面图路径')
    banner_url: Mapped[str] = mapped_column(String(255), nullable=True, comment='首页Banner路径')
    is_banner: Mapped[bool] = mapped_column(Boolean, default=False, comment='是否设为首页Banner图')
    is_notice: Mapped[bool] = mapped_column(Boolean, default=False, comment='是否notice资讯')
    type: Mapped[str] = mapped_column(
        String(16), default='notice', comment='类型：notice资讯，active活动'
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), comment='发布时间'
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间'
    )

    def __repr__(self) -> str:
        return f"<News id={self.id} title='{self.title}' type='{self.type}' created_at={self.created_at}>"
