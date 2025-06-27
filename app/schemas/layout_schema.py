from pydantic import BaseModel
from typing import Optional, List


class UserProfileUpdateForm(BaseModel):
    id: int
    avatar: str  # 用户头像路径（如果未上传就传默认）
    name: str  # 昵称
    introduction: str  # 简介


class UserProfileUpdateResult(BaseModel):
    avatar: str  # 头像
    nickname: str  # 昵称（同步到 userStore.nickname）
    signature: str  # 签名（同步到 userStore.signature）


class SearchBookRequest(BaseModel):
    keyword: Optional[str] = None  # 关键词（书名或作者）
    type: Optional[int] = 0  # 排序方式：0=相关，1=最热，2=最新
    timeindex: Optional[int] = 0  # 更新时间筛选索引：0=全部
    numindex: Optional[int] = 0  # 字数范围索引：0=全部
    stateindex: Optional[int] = 0  # 状态筛选索引：0=全部
    page: int  # 当前页码，必须 > 0
    pageSize: int  # 每页条数，最大建议不超过 100


class SearchBookItem(BaseModel):
    title: str
    author: str
    status: str
    wordCount: int
    intro: str
    updatedAt: str
    pic: str
    people: int
    update: str
    path: str
    readPath: str
    updatePath: str


class SearchBookResponse(BaseModel):
    total: int
    records: List[SearchBookItem]
