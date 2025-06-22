from pydantic import BaseModel
from typing import Optional, List

class AuthorApplyForm(BaseModel):
    id: int
    avatar: str
    name: str
    introduction: str

class AuthorApplyResult(BaseModel):
    avatar: str                    # 最终使用的头像路径（上传或默认）
    nickname: str                  # 作家笔名（同步到 userStore.nickname）
    become_author_at: Optional[str]  # 成为作者的时间（ISO 时间戳）
    signature: str                 # 签名（同步到 userStore.signature）

class AuthorStatsSchema(BaseModel):
    fans_count: int
    total_words: int

class NoticeItemSchema(BaseModel):
    notice_url: str
    title: str
    time: str
    path: str

class NewsListItemSchema(BaseModel):
    title: str
    path: str

class SortItem(BaseModel):
    num: int              # 榜单序号
    title: str            # 书名
    path: str             # 路径链接，如 /book/123
    pic: str              # 封面图片 URL
    author: str           # 作者名
    desc: str             # 简介内容

class BookRankResponse(BaseModel):
    plot_type: str                # 分类名，如“西方奇幻”
    child: List[SortItem]

from pydantic import BaseModel

class BookCreateForm(BaseModel):
    id: int
    name: str
    reader_type: str
    tag: str
    hero1: str = ''
    hero2: str = ''
    introduction: str

class MyBookListQuery(BaseModel):
    user_id: int

class BookListItem(BaseModel):
    title: str
    pic: str
    now: str
    chapter: int
    words: int
    status: str
    path: str

class BookListResponse(BaseModel):
    books: List[BookListItem]

class BookDetailSchema(BaseModel):
    id: int
    title: str
    cover_url: str
    target_readers: str
    tags: str
    main_roles: str
    intro: str
    created_at: str
    status: str
    contract_status: str
    update_status: str

class BookUpdateForm(BaseModel):
    book_id: int
    name: str
    reader_type: str
    tag: str
    hero: str
    introduction: str

class ChapterInfoSchema(BaseModel):
    volume_index: Optional[int] = 0              # 卷号
    volume_title: Optional[str] = ''             # 卷名称
    chapter_index: Optional[int] = 0             # 章节号
    chapter_title: Optional[str] = ''            # 章节标题

class ChapterCreateSchema(BaseModel):
    book_id: int
    volume_index: int
    chapter_num: int
    title: str
    content: str
    word_count: int

# 分卷信息（用于 select 下拉）
class VolumeItem(BaseModel):
    id: int
    book_id: int
    title: str
    sort: int
    created_at: str

# 章节信息（用于 table 表格）
class ChapterItem(BaseModel):
    id: int
    volume_id: int
    chapter_num: int
    title: str
    word_count: int
    updated_at: str
    status: Optional[str] = None
    status_text: Optional[str] = None
    typo_count: Optional[int] = 0

# 章节列表返回结构
class ChapterListResponse(BaseModel):
    title: str                    # 书名
    volumes: List[VolumeItem]     # 分卷列表
    list: List[ChapterItem]       # 章节列表

class ChapterUpdateSchema(BaseModel):
    book_id: int                # 所属书籍 ID
    chapter_id: int             # 当前章节 ID
    chapter_num: int            # 章节编号
    title: str                  # 标题
    content: str                # 正文内容
    word_count: int             # 字数
    is_draft: Optional[bool] = False

class ChapterDetailSchema(BaseModel):
    volume_index: int         # 卷序号（sort）
    volume_title: str         # 卷标题
    chapter_num: int          # 章节编号
    title: str                # 章节标题
    content: str              # 章节正文
