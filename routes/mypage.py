from flask import Flask, render_template, request, session, redirect, url_for
import sys
from datetime import datetime
from . import routes
from .db import mysql

@routes.route('/mypage', methods=['POST','GET'])
def mypage():
    
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT member_name, puppy_name, puppy_personality, walk_schedule, address_id FROM member WHERE member_id = '%s'" % session['user_member_id']
    cursor.execute(sql)
    data = cursor.fetchall()
    
    member_name = data[0][0]
    puppy_name = data[0][1]
    puppy_personality = data[0][2]
    walk_schedule = data[0][3]
    
    sql = "SELECT city, gu FROM address WHERE address_id = '%s'" %data[0][4]
    cursor.execute(sql)
    data_address = cursor.fetchall()
    city = data_address[0][0]
    gu = data_address[0][1]
    
    cursor.close()
    conn.close()
    return render_template("mypage.html", member_name=member_name, puppy_name=puppy_name, puppy_personality=puppy_personality, walk_schedule=walk_schedule, city=city, gu=gu)


@routes.route('/mypage_review', methods=['POST','GET'])
def mypage_review():
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql = "SELECT member_name, puppy_name, puppy_personality, walk_schedule, address_id FROM member WHERE member_id = '%s'" % session['user_member_id']
    cursor.execute(sql)
    data = cursor.fetchall()

    member_name = data[0][0]
    puppy_name = data[0][1]
    puppy_personality = data[0][2]
    walk_schedule = data[0][3]
    
    sql = "SELECT city, gu FROM address WHERE address_id = '%s'" % data[0][4]
    cursor.execute(sql)
    data_address = cursor.fetchall()
    city = data_address[0][0]
    gu = data_address[0][1]
    
    
    try:
        # 리뷰를 출력하기
        sql = "SELECT review_id, review_title, review_content, review_time, review_stars, place_id  FROM review WHERE member_id = '%s'" % session['user_member_id']
        cursor.execute(sql)
        data_review = cursor.fetchall()
        print("data_review:", data_review)  # data_review: (('test', 'test', datetime.datetime(2021, 12, 4, 20, 38), 5.0, 1), ('test2', 'test2', datetime.datetime(2021, 12, 10, 0, 0), 3.0, 2))
        review_id, review_title, review_content, review_time, review_stars, place_id = zip(*data_review)
        
        place_name_list = []
        for index, place in enumerate(place_id):
            sql = "SELECT place_name FROM place WHERE place_id = '%s'" % place
            cursor.execute(sql)
            data_place = cursor.fetchall()
            place_name_list.append(data_place[0][0])
            
        print("place_name_list: ", place_name_list)
        print("review_id: ", review_id)
        cursor.close()
        conn.close()
        
        
        return render_template("mypage_review.html", review_id = review_id,
                           review_count=len(review_title),
                           review_title=review_title,
                           review_content = review_content,
                           review_time = review_time,
                           review_stars = review_stars,
                           place_id = place_id,
                           place_name = place_name_list,
                           member_name=member_name, puppy_name=puppy_name, puppy_personality=puppy_personality, walk_schedule=walk_schedule, city=city, gu=gu)
    
    except:
        cursor.close()
        conn.close()

        return render_template("mypage_review.html", review_count=0,
                           member_name=member_name, puppy_name=puppy_name, puppy_personality=puppy_personality, walk_schedule=walk_schedule, city=city, gu=gu)

@routes.route('/mypage_posting', methods=['POST','GET'])
def mypage_posting():
    
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT member_name, puppy_name, puppy_personality, walk_schedule, address_id FROM member WHERE member_id = '%s'" % session['user_member_id']
    cursor.execute(sql)
    data = cursor.fetchall()
    
    member_name = data[0][0]
    puppy_name = data[0][1]
    puppy_personality = data[0][2]
    walk_schedule = data[0][3]
    
    sql = "SELECT city, gu FROM address WHERE address_id = '%s'" %data[0][4]
    cursor.execute(sql)
    data_address = cursor.fetchall()
    city = data_address[0][0]
    gu = data_address[0][1]
    
    
    try:
        sql = "SELECT post_id, post_title, post_content, post_time, place_id  FROM post WHERE member_id = '%s'" % session['user_member_id']
        cursor.execute(sql)
        data_post = cursor.fetchall()
        # print(data_post)
        post_id, post_title, post_content, post_time, place_id = zip(*data_post) # 열 데이터를 가져오기
        # print(review_post)
        
        place_name_list = []
        for index, place in enumerate(place_id):
            sql = "SELECT place_name FROM place WHERE place_id = '%s'" % place
            cursor.execute(sql)
            data_place = cursor.fetchall()
            place_name_list.append(data_place[0][0])
            
        
        cursor.close()
        conn.close()
        
        return render_template("mypage_posting.html", post_id = post_id,
                               post_count=len(post_title),
                               post_title=post_title,
                               post_content = post_content,
                               post_time = post_time,
                               place_id = place_id,
                               place_name = place_name_list,
                               member_name=member_name, puppy_name=puppy_name, puppy_personality=puppy_personality, walk_schedule=walk_schedule, city=city, gu=gu)
    
    except:
        cursor.close()
        conn.close()
        return render_template("mypage_posting.html",
                               post_count=0,
                               member_name=member_name, puppy_name=puppy_name, puppy_personality=puppy_personality, walk_schedule=walk_schedule, city=city, gu=gu)

    
@routes.route('/mypage_bookmark', methods=['POST','GET'])
def mypage_bookmark():
    
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT member_name, puppy_name, puppy_personality, walk_schedule, address_id FROM member WHERE member_id = '%s'" % session['user_member_id']
    cursor.execute(sql)
    data = cursor.fetchall()
    
    member_name = data[0][0]
    puppy_name = data[0][1]
    puppy_personality = data[0][2]
    walk_schedule = data[0][3]
    
    sql = "SELECT city, gu FROM address WHERE address_id = '%s'" %data[0][4]
    cursor.execute(sql)
    data_address = cursor.fetchall()
    city = data_address[0][0]
    gu = data_address[0][1]
    
    try:
        # 즐겨찾기를 출력하기
        sql = "SELECT bookmark_id, place_id FROM bookmark WHERE member_id = '%s'" % session['user_member_id']
        cursor.execute(sql)
        data_bookmark = cursor.fetchall()
        # print(data_bookmark)
        bookmark_id, place_id = zip(*data_bookmark) # 열 데이터를 가져오기

        # 장소 이름 찾기
        sql = "SELECT place_name FROM place WHERE place_id IN (SELECT place_id FROM bookmark WHERE member_id = '%s') " % session['user_member_id']
        cursor.execute(sql)
        data_place = cursor.fetchall()
        place_name = data_place

        cursor.close()
        conn.close()
        return render_template("mypage_bookmark.html",
                               bookmark_count = len(bookmark_id),
                               place_name = place_name,
                               bookmark_id = bookmark_id,
                               place_id = place_id,
                               member_name=member_name, puppy_name=puppy_name, puppy_personality=puppy_personality, walk_schedule=walk_schedule, city=city, gu=gu)
    except:
        return render_template("mypage_bookmark.html",
                               bookmark_count = 0,
                               member_name=member_name, puppy_name=puppy_name, puppy_personality=puppy_personality, walk_schedule=walk_schedule, city=city, gu=gu)

@routes.route('/mypage_comment', methods=['POST','GET'])
def mypage_comment():
# 유저 정보 패널
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT member_name, puppy_name, puppy_personality, walk_schedule, address_id FROM member WHERE member_id = '%s'" % session['user_member_id']
    cursor.execute(sql)
    data = cursor.fetchall()
    
    member_name = data[0][0]
    puppy_name = data[0][1]
    puppy_personality = data[0][2]
    walk_schedule = data[0][3]


    sql = "SELECT city, gu FROM address WHERE address_id = '%s'" %data[0][4]
    cursor.execute(sql)
    data_address = cursor.fetchall()
    city = data_address[0][0]
    gu = data_address[0][1]
    
    
    try:
        sql = "SELECT comment_content, post_id FROM comment WHERE member_id = '%s'" % session['user_member_id']
        cursor.execute(sql)
        data_post = cursor.fetchall()
        # print(data_post)
        comment_content, post_id = zip(*data_post) # 열 데이터를 가져오기
        print(post_id)
        
        post_title_list = []
        for index, post in enumerate(post_id):
            sql = "SELECT post_title FROM post WHERE post_id = '%s'" % post
            cursor.execute(sql)
            data_post = cursor.fetchall()
            post_title_list.append(data_post[0][0])
            
        
        cursor.close()
        conn.close()
        
        return render_template("mypage_comment.html", post_id = post_id,
                               comment_count=len(comment_content),
                               post_title=post_title_list,
                               comment_content=comment_content,
                               member_name=member_name, puppy_name=puppy_name, puppy_personality=puppy_personality, walk_schedule=walk_schedule, city=city, gu=gu)
    
    except:
        cursor.close()
        conn.close()
        return render_template("mypage_comment.html",
                               comment_count=0,
                               member_name=member_name, puppy_name=puppy_name, puppy_personality=puppy_personality, walk_schedule=walk_schedule, city=city, gu=gu)

    
@routes.route('/mypage/bookmark_insert', methods=['POST','GET'])
@routes.route('/mypage/bookmark_insert/<int:place_id>', methods=['POST','GET'])
def bookmark_insert(place_id=0):

    conn = mysql.connect()
    cursor = conn.cursor()
    
    # insert bookmark_id, member_id, place_id
    # bookmark_id -> count로
    # member_id -> session
    # place_id -> post_place_id
    
    
    member_id = session['user_member_id']
    
    sql = "SELECT COUNT(*) FROM bookmark WHERE member_id ="+str(member_id)+" AND place_id="+str(place_id)+";"
    cursor.execute(sql)
    data = cursor.fetchall()
    already = data[0][0]
    
    # 이미 즐겨찾기가 존재할 때
    if (already):
        cursor.close()
        conn.close()
        return redirect(url_for("routes.main_place", place_id=place_id))
    
    else:
        sql = "SELECT COUNT(*) FROM bookmark;"
        cursor.execute(sql)
        data = cursor.fetchall()
        bookmark_id = data[0][0] + 1

        sql = "INSERT INTO bookmark values(" + str(bookmark_id) + "," + str(member_id) + "," + str(place_id) + ");"
        cursor.execute(sql)

        new_data = cursor.fetchall()

        if not new_data:
            conn.commit()  # 변경사항 저장
            cursor.close()
            conn.close()
            return redirect(url_for("routes.main_place", place_id=place_id))
        else:
            conn.rollback()  # 데이터베이스에 대한 모든 변경사항을 되돌림
            cursor.close()
            conn.close()
            return redirect(url_for("routes.main_place", place_id=place_id))

        return redirect(url_for("routes.main_place", place_id=place_id))

    
@routes.route('/mypage/bookmark_delete', methods=['POST','GET'])
@routes.route('/mypage/bookmark_delete/<int:bookmark_id>', methods=['POST','GET'])
def bookmark_delete(bookmark_id=0):

    conn = mysql.connect()
    cursor = conn.cursor()
    
    member_id = session['user_member_id']
    
    sql = "SELECT member_name, puppy_name, puppy_personality, walk_schedule, address_id FROM member WHERE member_id = '%s'" % session['user_member_id']
    cursor.execute(sql)
    data = cursor.fetchall()
    
    member_name = data[0][0]
    puppy_name = data[0][1]
    puppy_personality = data[0][2]
    walk_schedule = data[0][3]
    
    sql = "SELECT city, gu FROM address WHERE address_id = '%s'" %data[0][4]
    cursor.execute(sql)
    data_address = cursor.fetchall()
    city = data_address[0][0]
    gu = data_address[0][1]
    
    sql = "SELECT COUNT(*) FROM bookmark;"
    cursor.execute(sql)
    data = cursor.fetchall()
    length = data[0][0]
    
    # 즐겨찾기를 지우는 함수
    sql = "DELETE FROM bookmark WHERE bookmark_id = %s;" % str(bookmark_id)
    cursor.execute(sql)
    conn.commit()
    
    
    for index in range(bookmark_id+1, length+1, 1):
        sql = "UPDATE bookmark SET bookmark_id = " + str(index-1) + " WHERE bookmark_id =" + str(index) + ";" 
        print(sql)
        cursor.execute(sql)
        conn.commit()
    
    
    sql = "SELECT bookmark_id, place_id FROM bookmark WHERE member_id = '%s'" % session['user_member_id']
    cursor.execute(sql)
    data_bookmark = cursor.fetchall()
    if(data_bookmark):
        bookmark_id, place_id = zip(*data_bookmark) # 열 데이터를 가져오기

        # 장소 이름 찾기
        sql = "SELECT place_name FROM place WHERE place_id IN (SELECT place_id FROM bookmark WHERE member_id = '%s') " % session['user_member_id']
        cursor.execute(sql)
        data_place = cursor.fetchall()
        place_name = data_place

        cursor.close()
        conn.close()   


        return render_template("mypage_bookmark.html",
                                   bookmark_count = len(bookmark_id),
                                   place_name = place_name,
                                   bookmark_id = bookmark_id,
                                   place_id = place_id,
                                   member_name=member_name, puppy_name=puppy_name, puppy_personality=puppy_personality, walk_schedule=walk_schedule, city=city, gu=gu)

    # 다 지우니 없다면
    else:
        return render_template("mypage_bookmark.html",
                                   bookmark_count = 0,
                                   member_name=member_name, puppy_name=puppy_name, puppy_personality=puppy_personality, walk_schedule=walk_schedule, city=city, gu=gu)
