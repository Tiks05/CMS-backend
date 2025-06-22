from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.extensions import db

class Volume(db.Model):
    __tablename__ = 'volume'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'), nullable=False, comment='所属书籍ID')
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment='卷标题')
    sort: Mapped[int] = mapped_column(Integer, default=0, comment='排序')
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), comment='创建时间')

    chapters = relationship('Chapter', back_populates='volume')

    book = relationship('Book', backref='volumes')

    def __repr__(self) -> str:
        return f"<Volume id={self.id} book_id={self.book_id} title='{self.title}' sort={self.sort}>"