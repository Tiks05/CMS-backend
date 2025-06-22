from pydantic import BaseModel
from typing import Optional

class PicNoticeSchema(BaseModel):
    cover_url: Optional[str]
    title: str
    path: str

class NoticeSchema(BaseModel):
    title: str
    path: str

class ActiveSchema(BaseModel):
    cover_url: Optional[str]
    title: str
    path: str
    updated_at: str

class ClassroomOutSchema(BaseModel):
    title: str
    intro: str
    cover_url: str
    path: str
    is_include_video: bool