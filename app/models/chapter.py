from sqlalchemy import String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.extensions import db


class Chapter(db.Model):
    __tablename__ = 'chapter'

    id: Mapped[int] = mapped_column(primary_key=True)

    volume_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('volume.id'), nullable=False, comment='所属卷ID'
    )

    chapter_num: Mapped[int] = mapped_column(Integer, nullable=False, comment='章节序号')
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment='章节标题')
    word_count: Mapped[int] = mapped_column(Integer, nullable=True, comment='章节字数')
    content: Mapped[str] = mapped_column(Text, nullable=False, comment='章节正文内容')

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default='published',
        server_default='published',
        comment='章节审核状态：published已发布、reviewing审核中、rejected未通过、pending待发布',
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), comment='创建时间'
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间'
    )

    volume = relationship("Volume", back_populates="chapters")

    def __repr__(self):
        return f"<Chapter {self.title} (Volume ID: {self.volume_id})>"
