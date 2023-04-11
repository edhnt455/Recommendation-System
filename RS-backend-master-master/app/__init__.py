# from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from Database import DB
app = Flask(__name__)
app.secret_key = "123456"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://hgg:123456@skyhook.cloud:3306/flask'   # 绑定mysql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "ssfbvhsjvsbvwahblvskbkd"

db = DB()  # 实例化的数据库

# 注册蓝图
from .api import user
app.register_blueprint(user, url_prefix='/user')