from pydantic import BaseModel
from typing import List


class AuthorSchema(BaseModel):
    nickname: str
    cover_url: str
    signature: str
    path: str


class BookSchema(BaseModel):
    id: int
    title: str
    cover_url: str
    status: str
    word_count: int
    tags: str
    updated_at: str
    latest_chapter: int
    latest_chapter_title: str


class BookHeaderSchema(BaseModel):
    book: BookSchema
    author: AuthorSchema


class ChapterSchema(BaseModel):
    title: str
    path: str


class VolumeSchema(BaseModel):
    title: str
    chapter_count: int
    chapters: List[ChapterSchema]


class BookContentSchema(BaseModel):
    intro: str
    volumes: List[VolumeSchema]


class ChapterReadResponse(BaseModel):
    book_title: str  # 小说名称
    chapter_title: str  # 章节标题（如：第1章 空屋）
    word_count: int  # 字数统计
    updated_at: str  # 更新时间（前端显示为 yyyy-mm-dd）
    content: str  # 正文内容（用 \n 分段）
    chapter_index: int
    prev_chapter_id: int | None = None
    next_chapter_id: int | None = None
