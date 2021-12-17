from flask import Flask, render_template, request, session, redirect, url_for, flash
import sys
from datetime import datetime
from . import routes
from .db import mysql

@routes.route('/main', methods=['POST','GET'])
def main(): # 메인 페이지 - 마이페이지, 장소 검색, 장소 등록, 게시글, 리뷰
    if session['user_member_id'] == None:
        return redirect(url_for('routes.login'))
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    # 게시글 및 리뷰 5개 출력 쿼리
    sql = "SELECT post_id, post_title, post_content FROM post ORDER BY post_time DESC LIMIT 5"
    
    cursor.execute(sql)
    data = cursor.fetchall()
    post_id, post_title, post_content = zip(*data)
    # print(post_title)
    
    sql = "SELECT review_id, review_title, review_stars, review_content FROM review ORDER BY review_time DESC LIMIT 5"
    
    cursor.execute(sql)
    data = cursor.fetchall()
    
    review_id, review_title, review_stars, review_content = zip(*data)
    
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
    
    cursor.close()
    conn.close()
    
    return render_template("main.html", 
                           user_member_name = session['user_member_name'],
                           city_len=len(city),
                           gu_len=len(gu),
                           city=city, gu=gu, city_id=city_id, address_id=address_id,
                           gu_city_id=gu_city_id,
                           place_len=len(place_id), place_name=place_name, place_id=place_id, place_address_id=place_address_id,
                           post_len=len(post_title), post_id=post_id, post_title=post_title, post_content=post_content, 
                           review_len=len(review_title), review_id=review_id, review_title=review_title, review_stars=review_stars, review_content=review_content)

@routes.route('/main/place/write/default', methods=['POST','GET'])
@routes.route('/main/place/write/<int:post_address_id>', methods=['POST','GET'])
def main_place_write(post_address_id=0):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT DISTINCT city, city_id FROM address"
    cursor.execute(sql)
    city, city_id = zip(*cursor.fetchall())
    # print(city, city_id)
    sql = "SELECT gu, city_id, address_id FROM address"
    cursor.execute(sql)
    gu, gu_city_id, address_id = zip(*cursor.fetchall())
    # print(gu, gu_city_id, address_id)
    
    if (post_address_id != 0):
        sql = "SELECT city_id FROM address WHERE address_id=%s" % post_address_id
        cursor.execute(sql)
        data = cursor.fetchall()
        selected_city_id = data[0][0]
        
        cursor.close()
        conn.close()
        return render_template("main_place_write.html", user_member_name = session['user_member_name'],
                           selected_city_id=selected_city_id,
                           selected_address_id=post_address_id,
                           city_len=len(city),
                           gu_len=len(gu),
                           city=city, gu=gu, city_id=city_id, address_id=address_id,
                           gu_city_id=gu_city_id,
                           )
    cursor.close()
    conn.close()
    return render_template("main_place_write.html", 
                           city_len=len(city),
                           gu_len=len(gu),
                           city=city, gu=gu, city_id=city_id, address_id=address_id, gu_city_id=gu_city_id)

@routes.route('/main/place/post', methods=['POST','GET'])
def main_place_post():
#     get으로 얻어온 것을 place_id에 삽입하기
    error = None
    if request.method == 'POST':
        place_name = request.form['place_name']
        member_id = session['user_member_id']
        place_stars = 0.0
        address_id = request.form['address']
        
        conn = mysql.connect()
        cursor = conn.cursor()
        
        sql = "SELECT COUNT(*) FROM place"
        cursor.execute(sql)
        data = cursor.fetchall()
        
        place_id = data[0][0] + 1
        
        sql = "INSERT INTO place (place_id, place_name, member_id, place_stars, address_id) VALUES (%s, %s, %s, %s, %s)"
        value = (place_id, place_name, member_id, place_stars, address_id)
        cursor.execute(sql, value)
        
        new_data = cursor.fetchall()
        if not new_data:
            conn.commit()  # 변경사항 저장
            return redirect(url_for("routes.main_place", place_id=place_id))
        else:
            conn.rollback()  # 데이터베이스에 대한 모든 변경사항을 되돌림
            return "Register Failed"
         
        cursor.close()
        conn.close()
        
    return main()

@routes.route('/main/place/<int:place_id>', methods=['POST','GET'])
def main_place(place_id):
    ####################################################################
    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql = "SELECT place_name, place_stars FROM place WHERE place_id=%s" % place_id
    cursor.execute(sql)
    place_name = cursor.fetchall()
    
    # 게시글 및 리뷰 5개 출력 쿼리
    sql = "SELECT post_id, post_title, post_content FROM post WHERE place_id=%s ORDER BY post_time DESC LIMIT 5 " % place_id
    
    cursor.execute(sql)
    data = cursor.fetchall()
    if (data):
        post_id, post_title, post_content = zip(*data)
        # print(post_title)

        sql = "SELECT review_id, review_title, review_stars, review_content FROM review WHERE place_id=%s ORDER BY review_time DESC LIMIT 5" % place_id
        cursor.execute(sql)
        data = cursor.fetchall()
        if(data):
            review_id, review_title, review_stars, review_content = zip(*data)
            
            place_stars = 0
            for i in review_stars:
                place_stars += i
            place_stars = place_stars/len(review_stars)
            
            cursor.close()
            conn.close()
            # return render_template("main_place.html", place_name=place_name)
            return render_template("main_place.html",place_id=place_id, place_name=place_name[0][0], place_stars=place_stars,
                                  post_len=len(post_title), post_id=post_id, post_title=post_title, post_content=post_content, 
                                   review_len=len(review_title), review_id=review_id, review_title=review_title, review_stars=review_stars, review_content=review_content)
        else:
            cursor.close()
            conn.close()
            # return render_template("main_place.html", place_name=place_name)
            return render_template("main_place.html",place_id=place_id, place_name=place_name[0][0], place_stars=place_name[0][1],
                                  post_len=len(post_title), post_id=post_id, post_title=post_title, post_content=post_content, 
                                   review_len=0, review_id=[], review_title=[], review_stars=[], review_content=[])
    else:
        cursor.close()
        conn.close()
        # return render_template("main_place.html", place_name=place_name)
        return render_template("main_place.html",place_id=place_id, place_name=place_name[0][0], place_stars=place_name[0][1],
                              post_len=0, post_id=[], post_title=[], post_content=[], 
                               review_len=0, review_id=[], review_title=[], review_stars=[], review_content=[])


@routes.route('/main/search/place', methods=['POST','GET'])
def main_search():
    if request.method == "POST":
        searchPlace = request.form['searchPlace']
        conn = mysql.connect()
        cursor = conn.cursor()
        
        sql = "SELECT place_id FROM place WHERE place_name LIKE %s;" % ("'%"+searchPlace+"%'")
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        
        if result:
            return redirect(url_for('routes.main_place', place_id=result[0][0]))
        if not result:
            flash("검색내용에 부합하는 장소 이름이 없습니다.")
            
        cursor.close()
        conn.close()
    return redirect(url_for('routes.main'))

@routes.route('/main/search/posting', methods=['POST','GET'])
def main_search_post():
    if request.method == "POST":
        searchPosting = request.form['searchPosting']
        conn = mysql.connect()
        cursor = conn.cursor()
        
        sql = "SELECT post_id FROM post WHERE post_title LIKE %s;" % ("'%"+searchPosting+"%'")
        cursor.execute(sql)
        result = cursor.fetchall()
        
        if result:
            return redirect(url_for('routes.posting', post_id=result[0][0]))
        if not result:
            flash("검색내용에 부합하는 게시글이 없습니다.")
            
        cursor.close()
        conn.close()
    return redirect(url_for('routes.main'))
        
# @routes.route('/main/search/<string:post_content>', methods=['POST','GET'])
# def main_place(post_content):
#     """
#     사용자 게시글 검색[제목]    
#     """
#     # main_search.html 사용
#     # string: post_content
#     # search_count = len(post_title), post_title, post_content, place_id, post_time 
#     ####################################################################
#     member_name = session['user_member_name']
    
#     conn = mysql.connect()
#     cursor = conn.cursor()
    
#     sql = "SELECT * FROM post WHERE post_title like %%s" % post_content
#     cursor.execute(sql)
#     place_name = cursor.fetchall()
    
#     # 게시글 및 리뷰 5개 출력 쿼리
#     sql = "SELECT post_id, post_title, post_content FROM post WHERE place_id=%s ORDER BY post_time DESC LIMIT 5 " % place_id
    
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     if (data):
#         post_id, post_title, post_content = zip(*data)
#         # print(post_title)

#         sql = "SELECT review_id, review_title, review_stars, review_content FROM review WHERE place_id=%s ORDER BY review_time DESC LIMIT 5" % place_id
#         cursor.execute(sql)
#         data = cursor.fetchall()
#         if(data):
#             review_id, review_title, review_stars, review_content = zip(*data)
#             cursor.close()
#             conn.close()
#             # return render_template("main_place.html", place_name=place_name)
#             return render_template("main_search.html",# place_id=place_id, place_name=place_name[0][0], place_stars=place_name[0][1],
#                                   post_len=len(post_title), post_id=post_id, post_title=post_title, post_content=post_content, 
#                                    review_len=len(review_title), review_id=review_id, review_title=review_title, review_stars=review_stars, review_content=review_content)
#         else:
#             cursor.close()
#             conn.close()
#             # return render_template("main_place.html", place_name=place_name)
#             return render_template("main_place.html",place_id=place_id, place_name=place_name[0][0], place_stars=place_name[0][1],
#                                   post_len=len(post_title), post_id=post_id, post_title=post_title, post_content=post_content, 
#                                    review_len=0, review_id=[], review_title=[], review_stars=[], review_content=[])
#     else:
#         cursor.close()
#         conn.close()
#         # return render_template("main_place.html", place_name=place_name)
#         return render_template("main_place.html",place_id=place_id, place_name=place_name[0][0], place_stars=place_name[0][1],
#                               post_len=0, post_id=[], post_title=[], post_content=[], 
#                                review_len=0, review_id=[], review_title=[], review_stars=[], review_content=[])
    