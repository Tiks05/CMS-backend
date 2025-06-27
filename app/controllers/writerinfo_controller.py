from flask import Blueprint
from app.services.writerinfo_service import get_writer_header_service, get_writer_works_service
from app.schemas.writerinfo_schema import WriterHeaderData, WriterWorksData
from app.core.response import Result  # 你统一返回格式

writerinfo_bp = Blueprint('writerinfo', __name__)


@writerinfo_bp.route('/header/<int:writer_id>', methods=['GET'])
def get_writer_header(writer_id):
    data = get_writer_header_service(writer_id)
    return Result.success(WriterHeaderData(writer=data).dict())


@writerinfo_bp.route('/works/<int:writer_id>', methods=['GET'])
def get_writer_works(writer_id):
    works = get_writer_works_service(writer_id)
    return Result.success(WriterWorksData(works=works).dict())
