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


@app.route('/', methods=['POST','GET'])
@app.route('/home', methods=['POST','GET'])
@app.route('/login', methods=['POST','GET'])
def login():
    
    return render_template("login.html") # 화면에 표시할 내용

# 로그인 실행
# 로그인 계정 정보는 post로 받아오지만
# 일반 리소스들은 get으로 받아오므로 get과 post모두 선언해줘야 한다.
@app.route('/sign_check', methods=['GET', 'POST'])
def login_check():
    error = None
    if request.method == 'POST':
        member_name = request.form['member_name']
        password = request.form['password']
        
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT member_name FROM member WHERE member_name = %s AND password = %s"
        value = (member_name, password)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)
    
        data = cursor.fetchall()
        cursor.close()
        conn.close()
    
        # for row in data:
            # data = row[0]

        if data:
            # session['login_user'] = user_name
            return main()
        else:
            # error = 'invalid input data detected !'
            return login()


@app.route('/join', methods=['POST','GET']) # URL과 함수 연결
def join():
    error = None
    count = 0
    print(request.method)
    if request.method == 'GET':
        id = request.form.get('join_id', False)
                
        pwd = request.form.get('join_pwd', False)
        puppy = request.form.get('join_puppy', False)
        puppy_pers = request.form.get('join_per', False)
        walk_cycle = request.form.get('join_cycle', False)
        
        address = request.form.get('address', False)
        
        conn = mysql.connect()
        cursor = conn.cursor()
        
        sql = "SELECT DISTINCT city, city_id FROM address"
        cursor.execute(sql)
        city, city_id = zip(*cursor.fetchall())
        sql = "SELECT gu, city_id, address_id FROM address"
        cursor.execute(sql)
        gu, gu_city_id, address_id = zip(*cursor.fetchall())
        print("test:     ", address)
        
        if (id and pwd and puppy and puppy_pers and walk_cycle and address):
            
            
            sql = "SELECT COUNT(*) FROM member"
            cursor.execute(sql)

            data = cursor.fetchall()


            if data:  # data를 잘 불러왔다면
                
                index = data[0][0] + 1
                #print(index)
                
                if (index > 1):  # member가 한명이라도 존재한다면,
                    sql = "SELECT * FROM member WHERE member_name = \'" + id + "\';" 
                    cursor.execute(sql)

                    test = cursor.fetchall()

                    if not test:  # 중복되지 않을 때. 
                        sql = "INSERT INTO member(member_id, password, member_name, puppy_name, puppy_personality, walk_schedule, address_id) VALUES(\'%s\', \'%s\', \'%s\', \'%s\',\'%s\',\'%s\',\'%s\')" % (str(index), pwd, id, puppy, puppy_pers, walk_cycle, city)
                        cursor.execute(sql)

                        insert_d = cursor.fetchall()

                        if not insert_d:
                            conn.commit()
                        else:
                            conn.rollback()

                        cursor.close()
                        conn.close()

                        return render_template("login.html", city_len=len(city),
                           gu_len=len(gu), city=city, gu=gu, city_id=city_id, address_id=address_id, gu_city_id=gu_city_id)
                    else:
                        print("중복된다.")
                        return render_template('join.html', test = "    중복됩니다!" ,city_len=len(city),
                           gu_len=len(gu), city=city, gu=gu, city_id=city_id, address_id=address_id, gu_city_id=gu_city_id)

            else:
                print("else")
                error = 'invalid input data detected !'

                cursor.close()
                conn.close()
        else:
            if count > 1:
                return render_template('join.html', test = "    입력되지 않은 값이 있습니다." , city_len=len(city),
                               gu_len=len(gu), city=city, gu=gu, city_id=city_id, address_id=address_id, gu_city_id=gu_city_id)
            else:
                count += 1
                return render_template('join.html', city_len=len(city),
                               gu_len=len(gu), city=city, gu=gu, city_id=city_id, address_id=address_id, gu_city_id=gu_city_id)
        cursor.close()
        conn.close()
    return render_template('login.html')

    # else:
    #     error = 'invalid input data detected !'
    #     if count > 0:
    #         return render_template('join.html', test = "    값을 입력하세요!", city_len=len(city),
    #                        gu_len=len(gu), city=city, gu=gu, city_id=city_id, address_id=address_id, gu_city_id=gu_city_id)
    #     else:
    #         count += 1
    #         return render_template('join.html', city_len=len(city),
    #                        gu_len=len(gu), city=city, gu=gu, city_id=city_id, address_id=address_id, gu_city_id=gu_city_id)
        
@app.route('/join_complete', methods=['POST','GET'])
def join_complete():
    return main()

@app.route('/main', methods=['POST','GET'])
def main():
    return render_template("main.html")

@app.route('/posting', methods=['POST','GET'])
def posting():
    return render_template("posting.html")

@app.route('/mypage', methods=['POST','GET'])
def mypage():
    return render_template("mypage.html")

@app.route('/mypage_review', methods=['POST','GET'])
def mypage_review():
    return render_template("mypage_review.html")

@app.route('/mypage_posting', methods=['POST','GET'])
def mypage_posting():
    return render_template("mypage_posting.html")

@app.route('/mypage_bookmark', methods=['POST','GET'])
def mypage_bookmark():
    return render_template("mypage_bookmark.html")

@app.route('/mypage_comment', methods=['POST','GET'])
def mypage_comment():
    return render_template("mypage_comment.html")


@app.route('/review', methods=['POST','GET'])
def review():
    return render_template("review.html")


@app.route('/user/<user_name>/<int:user_id>')
def user(user_name, user_id):
    return f'Hello, {user_name}({user_id})!'





if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)