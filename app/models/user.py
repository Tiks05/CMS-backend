from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func
from app.extensions import db

class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(11), unique=True, nullable=False, comment='手机号')
    password: Mapped[str] = mapped_column(String(60), nullable=True, comment='加密后的密码')
    nickname: Mapped[str] = mapped_column(String(16), nullable=True, comment='昵称')
    role: Mapped[str] = mapped_column(String(16), nullable=True, comment='用户角色（user/author/admin）')
    avatar: Mapped[str] = mapped_column(String(255), nullable=True, comment='头像路径')
    signature: Mapped[str] = mapped_column(String(255), nullable=True, comment='签名')
    life_photo: Mapped[str] = mapped_column(String(255), nullable=True, comment='生活照路径')
    masterpiece: Mapped[str] = mapped_column(String(64), nullable=True, comment='代表作')
    author_level: Mapped[str] = mapped_column(String(16), nullable=True, comment='作家等级')
    level: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment='作家数值等级（Lv.0 起）')
    become_author_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True, comment='成为作家的时间')  # 新增字段
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), comment='注册时间')

    def __repr__(self):
        return f"<User {self.phone} - {self.role}>"
