from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return '''
    <h1>이건 h1 제목</h1>
    <p>이건 p 본문 </p>
    <a href="https://flask.palletsprojects.com">Flask 홈페이지 바로가기</a>
    '''

@app.route('/user/<user_name>/<int:user_id>')
def user(user_name, user_id):
    return f'Hello, {user_name}({user_id})!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)  # debug=True -> 해당 파일의 코드를 수정할 때마다 Flask가 변경된 것을 다시 인식하고 다시 시작한다.