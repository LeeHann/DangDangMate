from flask import Flask, session, render_template, redirect, request, url_for
from flaskext.mysql import MySQL
 
mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'deu05232'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password311020*'
app.config['MYSQL_DATABASE_DB'] = 'Dang_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = "ABCDEFG"
mysql.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def main():
    error = None
    
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
 
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM member"
        # value = (id, pw)
        # cursor.execute("set names utf8")
        cursor.execute(sql)
 
        data = cursor.fetchall()
        cursor.close()
        conn.close()
 
        # for row in data:
        #     data = row[0]
 
        if data:
            # session['login_user'] = id  # 값이 남아있게 하는 함수
            print("****************",data)
            return redirect(url_for('home'))
        else:
            error = 'invalid input data detected !'
    return render_template('main_.html', error = error)

@app.route('/home.html', methods=['GET', 'POST'])
def home():
    error = None
    # id = session['login_user']
    return render_template('home_.html', error=error)

@app.route('/join', methods=['POST','GET']) # URL과 함수 연결
def join():
    return render_template("join.html") # 화면에 표시할 내용


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)