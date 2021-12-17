from flask import Flask, render_template, request, session, redirect, url_for
import sys
from datetime import datetime
from . import routes
from .db import mysql

@routes.route('/', methods=['POST','GET'])
@routes.route('/home', methods=['POST','GET'])
@routes.route('/login', methods=['POST','GET'])
def login():
    session.clear()
    return render_template("login.html") # 화면에 표시할 내용

# 로그인 실행
# 로그인 계정 정보는 post로 받아오지만
# 일반 리소스들은 get으로 받아오므로 get과 post모두 선언해줘야 한다.
@routes.route('/sign_check', methods=['GET', 'POST'])
def login_check():
    error = None
    if request.method == 'POST':
        member_name = request.form['member_name']
        password = request.form['password']
        
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT member_id, member_name FROM member WHERE member_name = %s AND password = %s"
        value = (member_name, password)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)
    
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        if data:
            session['user_member_id'] = data[0][0]
            session['user_member_name'] = member_name
            session['user_member_password'] = password
            return redirect(url_for('routes.main'))
        else:
            return render_template("login.html", warn="잘못된 입력입니다.")


@routes.route('/join', methods=['POST','GET']) # URL과 함수 연결
def join():
    error = None
    count = 0
    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql = "SELECT DISTINCT city, city_id FROM address"
    cursor.execute(sql)
    city, city_id = zip(*cursor.fetchall())
    # print(city, city_id)
    sql = "SELECT gu, city_id, address_id FROM address"
    cursor.execute(sql)
    gu, gu_city_id, address_id = zip(*cursor.fetchall())
    if request.method == 'GET':
        return render_template("join.html", 
                           city_len=len(city),
                           gu_len=len(gu),
                           city=city, gu=gu, city_id=city_id, address_id=address_id, gu_city_id=gu_city_id)
        
    if request.method == 'POST':
        id = request.form['join_id']
        pwd = request.form['join_pwd']
        puppy = request.form['join_puppy']
        puppy_pers = request.form['join_per']
        walk_cycle = request.form['join_cycle']
        address = request.form['address']
        # print(address)
        
        
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
                        sql = "INSERT INTO member(member_id, password, member_name, puppy_name, puppy_personality, walk_schedule, address_id) VALUES(\'%s\', \'%s\', \'%s\', \'%s\',\'%s\',\'%s\',\'%s\')" % (str(index), pwd, id, puppy, puppy_pers, walk_cycle, address)
                        cursor.execute(sql)

                        insert_d = cursor.fetchall()

                        if not insert_d:
                            conn.commit()
                        else:
                            conn.rollback()

                        cursor.close()
                        conn.close()

                        return redirect(url_for('routes.login'))
                    else:
                        # print("중복된다.")
                        return render_template('join.html', test = "    중복됩니다!",
                                               city_len=len(city),
                                               gu_len=len(gu),
                                               city=city, gu=gu, city_id=city_id, 
                                               address_id=address_id, gu_city_id=gu_city_id)

            else:
                # print("else")
                error = 'invalid input data detected !'

                cursor.close()
                conn.close()
        else:
            return render_template('join.html', test ="    입력되지 않은 값이 있습니다.",
                                  city_len=len(city),
                                  gu_len=len(gu),
                                  city=city, gu=gu, city_id=city_id, 
                                  address_id=address_id, gu_city_id=gu_city_id)

        
    else:
        error = 'invalid input data detected !'
        if count > 0:
            return render_template('join.html', test = "    값을 입력하세요!")
        else:
            count += 1
            return render_template('join.html')

@routes.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('routes.login'))