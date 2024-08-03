from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# import config

db = SQLAlchemy()
migrate = Migrate()


def page_not_found(e):
    return render_template('404.html'), 404


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, question_views, answer_views

    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    # 오류페이지
    app.register_error_handler(404, page_not_found)

    return app

# app는 객체 플라스크 애플리케이션을 생성코드객체
# __name__ 인수인데 모듈명을 담는 인수
# 즉, 이 파일이 실행되면 pybo.py가 모듈이 실행된다.
