from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.extensions import db
from sqlalchemy import ForeignKey


class Book(db.Model):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), nullable=False, comment='作者ID'
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment='小说名称')
    reader_type: Mapped[str] = mapped_column(String(8), nullable=True, comment='读者性别 男生/女生')
    theme_type: Mapped[str] = mapped_column(String(64), nullable=True, comment='主题分类标签')
    role_type: Mapped[str] = mapped_column(String(64), nullable=True, comment='角色分类标签')
    plot_type: Mapped[str] = mapped_column(String(64), nullable=True, comment='情节分类标签')
    hero: Mapped[str] = mapped_column(String(64), nullable=True, comment='主角名')
    status: Mapped[str] = mapped_column(String(16), nullable=True, comment='连载状态 已完结/连载中')
    word_count: Mapped[int] = mapped_column(Integer, nullable=True, comment='实际字数')
    word_count_range: Mapped[str] = mapped_column(String(20), nullable=True, comment='字数区间')
    tags: Mapped[str] = mapped_column(String(255), nullable=True, comment='标签')
    intro: Mapped[str] = mapped_column(Text, nullable=True, comment='简介')
    cover_url: Mapped[str] = mapped_column(String(255), nullable=True, comment='封面图片')
    favorite_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment='被收藏数量'
    )
    sign_status: Mapped[str] = mapped_column(
        String(16), default='未签约', comment='签约状态 未签约/已签约'
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), comment='创建时间'
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间'
    )

    author = relationship("User", backref="books")

    def __repr__(self):
        return f"<Book {self.title} by User {self.user_id}>"
