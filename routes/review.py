from flask import Flask, render_template, request, session, redirect, url_for
import sys
from datetime import datetime
from . import routes
from .db import mysql

@routes.route('/review/write', methods=['POST','GET'])
@routes.route('/review/write/<int:post_place_id>', methods=['POST','GET'])
def review_write(post_place_id=0):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # 장소 선택 쿼리
    sql = "SELECT DISTINCT city, city_id FROM address"
    cursor.execute(sql)
    city, city_id = zip(*cursor.fetchall())
    sql = "SELECT gu, city_id, address_id FROM address"
    cursor.execute(sql)
    gu, gu_city_id, address_id = zip(*cursor.fetchall())
    sql = "SELECT place_name, place_id, address_id FROM place"
    cursor.execute(sql)
    place_name, place_id, place_address_id = zip(*cursor.fetchall())
    # print(place_id)
    
    if (post_place_id != 0):
        print(f'place_id:{post_place_id}')
        sql = "SELECT address_id FROM place WHERE place_id=%s" % post_place_id
        cursor.execute(sql)
        data = cursor.fetchall()
        selected_place_id = post_place_id
        selected_address_id = data[0][0]
        # print(selected_address_id)
        sql = "SELECT city_id FROM address WHERE address_id=%s" % selected_address_id
        cursor.execute(sql)
        data = cursor.fetchall()
        selected_city_id = data[0][0]
        
        cursor.close()
        conn.close()
        return render_template("review_write.html", user_member_name = session['user_member_name'],
                           selected_city_id=selected_city_id,
                           selected_address_id=selected_address_id,
                           selected_place_id=selected_place_id,
                           city_len=len(city),
                           gu_len=len(gu),
                           city=city, gu=gu, city_id=city_id, address_id=address_id,
                           gu_city_id=gu_city_id,
                           place_len=len(place_id), place_name=place_name, place_id=place_id, place_address_id=place_address_id)

    cursor.close()
    conn.close()
    return render_template("review_write.html", user_member_name = session['user_member_name'],
                           city_len=len(city),
                           gu_len=len(gu),
                           city=city, gu=gu, city_id=city_id, address_id=address_id,
                           gu_city_id=gu_city_id,
                           place_len=len(place_id), place_name=place_name, place_id=place_id, place_address_id=place_address_id)
    
@routes.route('/review/post', methods=['POST','GET'])
def review_post():
    error = None
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        
        sql = "SELECT COUNT(*) FROM review"
        cursor.execute(sql)
        data = cursor.fetchall()
        
        review_id = data[0][0] + 1
        # print(review_id)
        review_title = request.form['review_title']
        review_content = request.form['review_content']
        now = datetime.now()
        review_time = now.strftime('%Y-%m-%d %H:%M:%S')
        
        review_stars = request.form['review_stars']
        
        member_id = session['user_member_id']
        place_id = request.form.get('post_place')
        
        sql = "INSERT INTO review (review_id, review_title, review_content, review_time, review_stars, member_id, place_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        value = (review_id, review_title, review_content, review_time, review_stars, member_id, place_id)
        cursor.execute(sql, value)
    
        new_data = cursor.fetchall()
        if not new_data:
            conn.commit()  # 변경사항 저장
            return redirect(url_for("routes.main"))
        else:
            conn.rollback()  # 데이터베이스에 대한 모든 변경사항을 되돌림
            return "Register Failed"
         
        cursor.close()
        conn.close()

@routes.route('/review/<int:review_id>', methods=['POST','GET'])
def review(review_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT review_title, member_id, review_content, review_time, review_stars, place_id, review_id FROM review WHERE review_id = '%s'" % (review_id)
    cursor.execute(sql)
    
    data = cursor.fetchall()
    review_title = data[0][0]
    
    sql = "SELECT member_name FROM member WHERE member_id = '%s'" % (data[0][1])
    cursor.execute(sql)
    data_name = cursor.fetchall()
    member_name = data_name[0][0]
    
    session_name = session['user_member_name']
    auth = False
    if session_name == member_name:
        auth = True
    if session_name == 'root':
        auth = True
    
    review_content = data[0][2]
    review_time = data[0][3]
    review_stars = data[0][4]
    place_id = data[0][5]
    review_id = data[0][6]
    
    sql = "SELECT place_name FROM place WHERE place_id = %s;" % place_id
    cursor.execute(sql)
    place_name = cursor.fetchall()[0][0]

    
    cursor.close()
    conn.close()
    
    return render_template("review.html", auth=auth, review_id=review_id, review_title=review_title, review_stars=review_stars, member_name=member_name, review_content=review_content, place_name=place_name)

@routes.route('/review/delete', methods=['POST','GET'])
@routes.route('/review/delete/<int:id>', methods=['POST','GET'])
def review_delete(id):
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # 전체 길이 구하고
    sql = "SELECT COUNT(*) FROM review;"
    cursor.execute(sql)
    data = cursor.fetchall()
    length = data[0][0]
    
    # 게시물을 지우는 함수
    sql = "DELETE FROM review WHERE review_id = %s;" % id
    cursor.execute(sql)
    conn.commit()
    
    # id값부터 post_id를 -1씩 빼면서 update 함.
    # ex 1 ~ 6개의 data -> index 2가 삭제됐다면, index 3부터 6까지 update  
    if length != id:
        for index in range(id+1, length+1, 1):
            sql = "UPDATE review SET review_id = " + str(index-1) + " WHERE review_id =" + str(index) + ";" 
            print(sql)
            cursor.execute(sql)
            conn.commit()
    
    
    cursor.close()
    conn.close()    
    
    return redirect(url_for("routes.mypage_review"))