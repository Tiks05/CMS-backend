from typing import List, Optional
from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str
    avatar: str

class CommentChild(BaseModel):
    id: int
    content: str
    time: str
    likes: int
    parent_id: Optional[int] = None
    reply_to_user: Optional[UserInfo] = None
    user: UserInfo

class CommentResponse(BaseModel):
    id: int
    content: str
    time: str
    likes: int
    user: UserInfo
    children: List[CommentChild] = []

class LikeUpdateRequest(BaseModel):
    ids: List[int]

class CreateCommentRequest(BaseModel):
    user_id: int                      # 前端传递的用户 ID
    book_id: int                      # 所属书籍ID
    content: str                      # 评论内容
    parent_id: Optional[int] = None   # 父评论ID（如果是回复则有）
    reply_to_user_id: Optional[int] = None  # 被@的用户 ID（替代昵称）
