from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return 'hi'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
# 출처: https://dubaiyu.tistory.com/127 [프론트엔드 여행하려다 풀스택:티스토리]
