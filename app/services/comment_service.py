import datetime
from typing import List, Dict
from flask import request
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.models.comment import Comment
from collections import defaultdict
from app.schemas.comment_schema import CommentResponse, CommentChild, UserInfo, CreateCommentRequest
from collections import defaultdict
from flask import request
from typing import List, Dict
from sqlalchemy.orm import joinedload
from app.models.comment import Comment
from app.extensions import db


def get_comments_by_book(book_id: int) -> List[Dict]:
    # 获取所有评论
    all_comments = (
        db.session.query(Comment)
        .options(joinedload(Comment.user), joinedload(Comment.reply_to_user))
        .filter(Comment.book_id == book_id)
        .order_by(Comment.created_at.asc())
        .all()
    )

    # 构建映射
    comment_dict = {c.id: c for c in all_comments}
    children_map = defaultdict(list)
    top_level_comments = []

    for comment in all_comments:
        if comment.parent_id:
            children_map[comment.parent_id].append(comment)
        else:
            top_level_comments.append(comment)

    # 构建平铺评论树（只展示一级 + 所有后代合并）
    def flatten_comment_tree(parent: Comment) -> List[Dict]:
        result = []

        for child in children_map.get(parent.id, []):
            parent_user_id = parent.user.id if parent else None

            item = {
                "id": child.id,
                "content": child.content,
                "time": child.created_at.strftime('%Y-%m-%d %H:%M'),
                "likes": child.likes,
                "parent_id": child.parent_id,
                "is_flat": (
                    child.reply_to_user_id is not None and child.reply_to_user_id != parent_user_id
                ),
                "reply_to_user": (
                    {
                        "id": child.reply_to_user.id,
                        "name": child.reply_to_user.nickname,
                        "avatar": (
                            f"{request.host_url.rstrip('/')}{child.reply_to_user.avatar}"
                            if child.reply_to_user.avatar
                            else ''
                        ),
                    }
                    if child.reply_to_user
                    else None
                ),
                "user": {
                    "id": child.user.id,
                    "name": child.user.nickname,
                    "avatar": (
                        f"{request.host_url.rstrip('/')}{child.user.avatar}"
                        if child.user.avatar
                        else ''
                    ),
                },
            }

            result.append(item)

            # 递归收集后代评论
            result.extend(flatten_comment_tree(child))

        return result

    # 构造结果列表
    results = []
    for top in top_level_comments:
        item = {
            "id": top.id,
            "content": top.content,
            "time": top.created_at.strftime('%Y-%m-%d %H:%M'),
            "likes": top.likes,
            "parent_id": None,
            "is_flat": False,
            "reply_to_user": None,
            "user": {
                "id": top.user.id,
                "name": top.user.nickname,
                "avatar": (
                    f"{request.host_url.rstrip('/')}{top.user.avatar}" if top.user.avatar else ''
                ),
            },
            "children": flatten_comment_tree(top),  # 所有子评论都平铺在这
        }
        results.append(item)

    return results


def increase_likes_by_ids(ids: List[int]) -> None:
    """
    批量点赞：将传入的 comment ID 列表对应的点赞数 +1
    """
    if not ids:
        return

    # 遍历每条更新（适合少量点赞）
    for cid in ids:
        db.session.query(Comment).filter_by(id=cid).update({Comment.likes: Comment.likes + 1})

    db.session.commit()


def create_comment(data: CreateCommentRequest) -> None:
    comment = Comment(
        user_id=data.user_id,
        book_id=data.book_id,
        content=data.content,
        parent_id=data.parent_id,
        reply_to_user_id=data.reply_to_user_id,
        created_at=datetime.datetime.now(),
    )
    db.session.add(comment)
    db.session.commit()
