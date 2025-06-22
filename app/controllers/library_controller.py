from flask import Blueprint, request
from app.schemas.library_schema import BookListQuerySchema
from app.services.library_service import get_filtered_books
from app.core.response import Result

library_bp = Blueprint('library', __name__)

@library_bp.route('/books', methods=['GET'])
def get_books():
    query_data = BookListQuerySchema(**request.args.to_dict())

    result = get_filtered_books(query_data)
    return Result.success(result)
