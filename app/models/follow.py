from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint, func
from app.extensions import db

class Follow(db.Model):
    __tablename__ = 'follow'

    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment='关注者ID（谁去关注别人）')
    followed_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment='被关注者ID（被谁关注）')
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), comment='关注时间')

    __table_args__ = (UniqueConstraint('follower_id', 'followed_id', name='uniq_follow'),)

    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id], backref="following")
    followed: Mapped["User"] = relationship("User", foreign_keys=[followed_id], backref="followers")

    def __repr__(self):
        return f"<Follow follower_id={self.follower_id} followed_id={self.followed_id}>"
