from flask import Blueprint, url_for, current_app
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, P!'


@bp.route('/')
def index():
    # 3/0 # 강제로 오류발생
    current_app.logger.info("INFO 레벨로 출력")
    return redirect(url_for('question._list'))


'''
bp 객체 생성시 사용된 __name__은 모듈명인 'main_views'가 인수로 
첫번째 인수로 전달한 "main"은 블루프린트의 별칭
url 앞에 기본으로 붙일 접두어 url을 의미
'''
