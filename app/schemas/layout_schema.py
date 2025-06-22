from pydantic import BaseModel
from typing import Optional

class UserProfileUpdateForm(BaseModel):
    id: int
    avatar: str                    # 用户头像路径（如果未上传就传默认）
    name: str                  # 昵称
    introduction: str              # 简介

class UserProfileUpdateResult(BaseModel):
    avatar: str                    # 头像
    nickname: str                  # 昵称（同步到 userStore.nickname）
    signature: str                 # 签名（同步到 userStore.signature）