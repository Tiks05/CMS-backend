from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint, func
from app.extensions import db


class Favorite(db.Model):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), nullable=False, comment='收藏者ID'
    )
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('book.id'), nullable=False, comment='被收藏的小说ID'
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), comment='收藏时间'
    )

    __table_args__ = (UniqueConstraint('user_id', 'book_id', name='uniq_favorite'),)

    user: Mapped["User"] = relationship("User", backref="favorites")
    book: Mapped["Book"] = relationship("Book", backref="favorited_users")

    def __repr__(self):
        return f"<Favorite user_id={self.user_id} book_id={self.book_id}>"
