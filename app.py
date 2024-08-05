# app.py
from flask import Flask, render_template

# Flask 객체 인스턴스 생성
app = Flask(__name__)


@app.route("/")
def home():
    return 'hi'

if __name__ == "__main__":
    app.run(host="192.168.0.99", port="5000", debug=True)
    # host 등을 직접 지정하고 싶다면
    # app.run(host="127.0.0.1", port="5000", debug=True)
