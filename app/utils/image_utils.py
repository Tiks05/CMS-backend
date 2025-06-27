import os
from uuid import uuid4
from flask import request
from werkzeug.datastructures import FileStorage
from app.config import BASE_DIR


def save_uploaded_image(
    file: FileStorage, sub_folder: str, upload_dir: str = 'static/uploads'
) -> tuple[str, str]:
    """
    保存上传的图片文件，返回 (相对路径, 前端可访问的完整URL)

    :param file: 上传的图片文件对象
    :param upload_dir: 静态资源上传根目录
    :param sub_folder: 子目录（例如 user/avatars）
    :return: (用于数据库的路径, 用于前端展示的URL)
    """
    ext = os.path.splitext(file.filename)[1]  # 扩展名
    filename = f"{uuid4().hex}{ext}"  # 随机文件名
    relative_path = f"/{upload_dir}/{sub_folder}/{filename}"
    save_path = os.path.join(BASE_DIR, relative_path.lstrip('/'))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 创建父目录
    file.save(save_path)  # 保存文件

    url_path = f"{request.host_url.rstrip('/')}{relative_path}"
    return relative_path, url_path
