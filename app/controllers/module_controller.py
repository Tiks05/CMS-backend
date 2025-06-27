from flask import Blueprint, request
from app.core.response import Result
from app.services.module_service import get_banner_list

module_bp = Blueprint('module', __name__)


@module_bp.route('/banner-list', methods=['GET'])
def banner_list():
    limit = int(request.args.get('limit', 5))
    banners = get_banner_list(limit)
    return Result.success(banners)
