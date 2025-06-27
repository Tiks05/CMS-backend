from sqlalchemy import String, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.extensions import db


class Classroom(db.Model):
    __tablename__ = 'classroom'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment='主标题')
    category_type: Mapped[str] = mapped_column(
        String(50), nullable=True, comment='分类标签'
    )  # 如 live / writing 等
    cover_url: Mapped[str] = mapped_column(String(255), nullable=True, comment='封面图路径')
    intro: Mapped[str] = mapped_column(String(255), nullable=True, comment='简介/摘要')
    is_include_video: Mapped[bool] = mapped_column(
        Boolean, default=False, comment='是否展示视频按钮'
    )
    content: Mapped[str] = mapped_column(Text, nullable=True, comment='HTML内容，含视频或正文')
    create_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), comment='创建时间'
    )

    def __repr__(self):
        return f"<Classroom id={self.id} title='{self.title}'>"
