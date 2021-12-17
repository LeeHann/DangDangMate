from flask import Flask, render_template, request, session, redirect, url_for
import sys
from flaskext.mysql import MySQL
from routes.db import mysql
from routes import *
from datetime import datetime

app = Flask(__name__) # flask 객체 가져오기
app.register_blueprint(routes)

app.config['MYSQL_DATABASE_USER'] = 'hanna'
app.config['MYSQL_DATABASE_PASSWORD'] = '39398435'
app.config['MYSQL_DATABASE_DB'] = 'Dang_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = "ABCDEFG"
mysql.init_app(app)

user_member_id = 0
user_member_name = ""
user_member_password = ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000) # 구름IDE에서는 이렇게 설정