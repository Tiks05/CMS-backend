import traceback
from flask import jsonify, request, current_app
from werkzeug.exceptions import BadRequest, MethodNotAllowed, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError


# 自定义业务异常
class APIException(Exception):
    def __init__(self, message='业务异常', code=40000, data=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self):
        return {"code": self.code, "message": self.message, "data": self.data}


# 注册全局异常处理器
def register_error_handlers(app):
    # 业务异常
    @app.errorhandler(APIException)  # 注册全局异常函数
    def handle_api_exception(e: APIException):
        current_app.logger.warning(f"[业务异常] {e.message}")
        return jsonify(e.to_dict()), 200

    # 请求参数校验异常（Marshmallow用）
    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        current_app.logger.warning(f"[参数校验失败] {e.messages}")
        return jsonify({"code": 40001, "message": f"参数校验失败：{e.messages}", "data": None}), 200

    # 请求参数格式错误
    @app.errorhandler(BadRequest)
    def handle_bad_request(e: BadRequest):
        current_app.logger.warning(f"[请求参数错误] {e.description}")
        return jsonify({"code": 40002, "message": "请求参数错误", "data": None}), 200

    # 请求方式不支持
    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(e: MethodNotAllowed):
        current_app.logger.warning(f"[请求方式不支持] method={request.method}")
        return (
            jsonify({"code": 40500, "message": f"请求方式不支持：{request.method}", "data": None}),
            200,
        )

    # 数据库异常
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(e: SQLAlchemyError):
        current_app.logger.error(f"[数据库异常]\n{traceback.format_exc()}")
        return (
            jsonify({"code": 50010, "message": "数据库操作异常，请联系管理员", "data": None}),
            200,
        )

    # 标准 HTTP 异常 (非常重要：解决静态文件问题的关键)
    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        # 保留HTTP异常原始响应（如404、403、405等）
        return e

    # 其他未知异常兜底
    @app.errorhandler(Exception)
    def handle_generic_exception(e: Exception):
        current_app.logger.error(f"[系统异常]\n{traceback.format_exc()}")
        return jsonify({"code": 50000, "message": "系统异常，请稍后再试", "data": None}), 200
