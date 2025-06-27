from pydantic import BaseModel
from typing import Optional, List


class BookListQuerySchema(BaseModel):
    reader_type: Optional[str]
    category_group: Optional[str]  # 'theme_type' | 'role_type' | 'plot_type'
    category_type: Optional[str]
    status: Optional[str]
    word_count_range: Optional[str]
    sort: Optional[str]  # 'hot' | 'new' | 'words'
    page: int = 1
    pageSize: int = 10


class BookOutSchema(BaseModel):
    id: int
    title: str
    author: str
    status: str
    wordCount: int
    intro: str
    coverUrl: str
    updatedAt: str
    path: str


class BookListOutSchema(BaseModel):
    total: int
    records: List[BookOutSchema]
