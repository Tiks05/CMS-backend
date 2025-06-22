from pydantic import BaseModel
from typing import List

class TopBookOut(BaseModel):
    num: str
    title: str
    desc: str
    path: str
    pic: str

class NewsOut(BaseModel):
    title: str
    path: str

class WriterOut(BaseModel):
    title: str
    desc: str
    type: str
    pic: str
    path: str

class BookOut(BaseModel):
    id: int
    title: str
    desc: str
    cover_url: str
    author_nickname: str
    path: str

class RecommendResponse(BaseModel):
    male: list[BookOut]
    female: list[BookOut]

class AdaptBookOut(BaseModel):
    id: int
    pic: str
    path: str

class AdaptListResponse(BaseModel):
    data: list[AdaptBookOut]

class RankingBookOut(BaseModel):
    num: str
    title: str
    desc: str
    path: str
    pic: str
    author: str

class BookRankingOut(BaseModel):
    plot_type: str  # 类别名（如：西方奇幻）
    child: List[RankingBookOut]     # 阅读榜
    new_child: List[RankingBookOut]  # 新书榜