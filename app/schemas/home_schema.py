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
    child: List[RankingBookOut]  # 阅读榜
    new_child: List[RankingBookOut]  # 新书榜


class RecentUpdateItem(BaseModel):
    type: str  # 分类（如：都市、悬疑）
    title: str  # 书名
    path: str  # 前端跳转路径（如 /bookinfo/1080）
    chapter: str  # 最新章节标题（如 第12章 xxx）
    author: str  # 作者名
    time: str  # 更新时间（格式化后的字符串）


class RecentUpdateResponse(BaseModel):
    updates: List[RecentUpdateItem]
