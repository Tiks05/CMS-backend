from pydantic import BaseModel
from typing import List, Optional

class Writer(BaseModel):
    nickname: str
    avatar_url: str
    signature: str
    intro: str
    become_author_at: str  # 建议格式为 ISO 日期字符串
    total_words: int
    follower_count: int
    # 你还可以继续加需要的字段

class WriterHeaderData(BaseModel):
    writer: Writer

class Work(BaseModel):
    title: str
    cover_url: str
    status: str
    word_count: int
    tags: str
    intro: str
    updated_at: Optional[str] = None
    bookinfo_path: str
    max_chapter: Optional[int] = None
    max_chapter_title: Optional[str] = None

class WriterWorksData(BaseModel):
    works: List[Work]
