from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, Text, ForeignKey, func
from app.extensions import db
from app.models.user import User
from app.models.book import Book


class Comment(db.Model):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), nullable=False, comment='评论者ID'
    )
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('book.id'), nullable=False, comment='小说ID'
    )
    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('comment.id'), nullable=True, comment='父评论ID（用于楼中楼回复）'
    )
    reply_to_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), nullable=True, comment='被@用户ID'
    )
    likes: Mapped[int] = mapped_column(Integer, default=0, nullable=True, comment='点赞数')

    content: Mapped[str] = mapped_column(Text, nullable=False, comment='评论内容')
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), comment='评论时间'
    )

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], backref="comments")
    reply_to_user: Mapped["User"] = relationship(
        "User", foreign_keys=[reply_to_user_id], backref="replied_comments"
    )

    # 其他关系
    book: Mapped["Book"] = relationship("Book", backref="comments")
    parent: Mapped["Comment"] = relationship("Comment", remote_side=[id], backref="replies")

    def __repr__(self):
        return f"<Comment id={self.id} user_id={self.user_id} book_id={self.book_id}>"
