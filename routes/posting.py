from flask import Flask, render_template, request, session, redirect, url_for
import sys
from datetime import datetime
from . import routes
from .db import mysql

@routes.route('/posting/write', methods=['POST','GET'])
@routes.route('/posting/write/<int:post_place_id>', methods=['POST','GET'])
def posting_write(post_place_id=0): # index = 게시글 번호
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
        return render_template("posting_write.html", user_member_name = session['user_member_name'],
                           selected_city_id=selected_city_id,
                           selected_address_id=selected_address_id,
                           selected_place_id=selected_place_id,
                           city_len=len(city),
                           gu_len=len(gu),
                           city=city, gu=gu, city_id=city_id, address_id=address_id,
                           gu_city_id=gu_city_id,
                           place_len=len(place_id), place_name=place_name, place_id=place_id, place_address_id=place_address_id)
    # 메인페이지에서 지역 선택 안 하고 게시글 쓰기를 눌렀을 때 - 지역 select가 선택되지 않은 posting_write 페이지가 나온다
    cursor.close()
    conn.close()    
    return render_template("posting_write.html", user_member_name = session['user_member_name'],
                           city_len=len(city),
                           gu_len=len(gu),
                           city=city, gu=gu, city_id=city_id, address_id=address_id,
                           gu_city_id=gu_city_id,
                           place_len=len(place_id), place_name=place_name, place_id=place_id, place_address_id=place_address_id)


@routes.route('/posting/delete', methods=['POST','GET'])
@routes.route('/posting/delete/<int:id>', methods=['POST','GET'])
def posting_delete(id):
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # 전체 길이 구하고
    sql = "SELECT COUNT(*) FROM post;"
    cursor.execute(sql)
    data = cursor.fetchall()
    length = data[0][0]
    
    # 게시물을 지우는 함수
    sql = "DELETE FROM post WHERE post_id = %s;" % id
    cursor.execute(sql)
    conn.commit()
    
    # id값부터 post_id를 -1씩 빼면서 update 함.
    # ex 1 ~ 6개의 data -> index 2가 삭제됐다면, index 3부터 6까지 update  
    if length != id:
        for index in range(id+1, length+1, 1):
            sql = "UPDATE post SET post_id = " + str(index-1) + " WHERE post_id =" + str(index) + ";" 
            print(sql)
            cursor.execute(sql)
            conn.commit()
    
    
    cursor.close()
    conn.close()    
    
    return redirect(url_for("routes.mypage_posting"))



@routes.route('/posting/post', methods=['POST','GET'])
def posting_post():
    error = None
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        
        sql = "SELECT COUNT(*) FROM post"
        cursor.execute(sql)
        data = cursor.fetchall()
        
        post_id = data[0][0] + 1
        # print(post_id)
        post_title = request.form['post_title']
        post_content = request.form['post_content']
        now = datetime.now()
        post_time = now.strftime('%Y-%m-%d %H:%M:%S')
        member_id = session['user_member_id']
        place_id = request.form.get('post_place')
        
        sql = "INSERT INTO post (post_id, post_title, post_time, post_content, member_id, place_id) VALUES (%s, %s, %s, %s, %s, %s)"
        value = (post_id, post_title,post_time, post_content, member_id, place_id)
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
        

@routes.route('/posting/<int:post_id>', methods=['POST','GET'])
def posting(post_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT post_title, member_id, place_id, post_time, post_content FROM post WHERE post_id = '%s'" % (post_id)
    cursor.execute(sql)
    
    data = cursor.fetchall()
    post_title = data[0][0]
    
    # print(f'member_id : {data[0][1]}')
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
    
    if data[0][2]:
        sql = "SELECT place_name FROM place WHERE place_id = '%s'" % (data[0][2])    # place_id => place_name
        cursor.execute(sql)
        data_address = cursor.fetchall()
        address = data_address[0][0]
    else :
        address = "장소가 정해지지 않았습니다."
        
    post_time = data[0][3]
    post_content = data[0][4]
    
    sql = "SELECT member_id, comment_content FROM comment WHERE post_id=%s" % post_id
    cursor.execute(sql)
    comment_data = cursor.fetchall()
    if comment_data:
        members_id, comment_content = zip(*comment_data)
    
        members_name = []
        for i in members_id:
            sql = "SELECT member_name FROM member WHERE member_id=%s" % i
            cursor.execute(sql)
            members_name.append(cursor.fetchall()[0][0])
            print("members_name: ", members_name)
        
    # sql = "SELECT member_name FROM member"
    # cursor.execute(sql)
    # members_name = cursor.fetchall()
    # print(members_name)
    
        cursor.close()
        conn.close()
        return render_template("posting.html", auth=auth, post_id=post_id,
                           members_name=members_name, comment_content=comment_content, comment_len=len(comment_content),
                           post_title=post_title, member_name=member_name, address=address, post_time=post_time, post_content=post_content)
    # return render_template("posting.html")
    cursor.close()
    conn.close()
    return render_template("posting.html", auth=auth, post_id=post_id,
                           post_title=post_title, member_name=member_name, address=address, post_time=post_time, post_content=post_content)

@routes.route('/posting/comment/<int:post_id>', methods=['POST','GET'])
def posting_comment(post_id):
    if request.method=="POST":
        # 댓글 내용 및 사용자 세션 정보, post_id, comment_id를 디비에 저장 후 게시글 리로드
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM comment"
        cursor.execute(sql)
        data = cursor.fetchall()
        
        comment = request.form['comment']
        member_id = session['user_member_id']
        comment_id = data[0][0] +1
        
        sql = "INSERT INTO comment (comment_id, comment_content, post_id, member_id) VALUES (%s, %s, %s, %s)"
        value = (comment_id, comment, post_id, member_id)
        cursor.execute(sql, value)
        data = cursor.fetchall()
        
        if not data:
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('routes.posting', post_id=post_id))   
        else:
            conn.rollback()
            return "comment insert Failed"
        cursor.close()
        conn.close()
    return redirect(url_for('routes.posting', post_id=post_id))