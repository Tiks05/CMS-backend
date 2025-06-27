from .auth_controller import auth_bp
from .home_controller import home_bp
from .library_controller import library_bp
from .writer_controller import writer_bp
from .module_controller import module_bp
from .workspace_controller import workspace_bp
from .layout_controller import layout_bp
from .bookinfo_controller import bookinfo_bp
from .writerinfo_controller import writerinfo_bp
from .comment_controller import comment_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth/login_or_register')
    app.register_blueprint(home_bp, url_prefix='/api/home')
    app.register_blueprint(library_bp, url_prefix='/api/library')
    app.register_blueprint(writer_bp, url_prefix='/api/writer')
    app.register_blueprint(module_bp, url_prefix='/api/module')
    app.register_blueprint(workspace_bp, url_prefix='/api/workspace')
    app.register_blueprint(layout_bp, url_prefix='/api/layout')
    app.register_blueprint(bookinfo_bp, url_prefix='/api/bookinfo')
    app.register_blueprint(writerinfo_bp, url_prefix='/api/writerinfo')
    app.register_blueprint(comment_bp, url_prefix='/api/comment')
