import pymysql
import pandas as pd
import numpy as np
import random

from pandas import DataFrame


class DB:
    def __init__(self):
        # 连接数据库
        self.conn = pymysql.connect(
            host='skyhook.cloud',
            user='hgg',
            passwd='123456',
            db='question',  # 数据库名称
            port=3306,
            charset='utf8')  # db:表示数据库名称
        # 使用cursor()方法创建一个游标对象
        self.cur = self.conn.cursor()
    def insert_record(self, record_list):
        # 使用cursor()方法创建一个游标对象
        print(record_list)
        self.cur = self.conn.cursor()  # 先建立一个游标对象
        final_update = "update record set final_exam = 6 where username = '"+record_list[1]+"'"
        exam_update = "update record set exam = 10 where username = " + record_list[1]
        recommend_update = "update record set recommend = 10 where username = " + record_list[1]
        leng_update = "update record set leng_exam = 10 where username = " + record_list[1]
        if record_list[0] == 'final_exam':
            self.cur.execute(final_update)
        elif record_list[0] == 'exam_exam':
            self.cur.execute(exam_update)
        elif record_list[0] == 'recommend':
            self.cur.execute(recommend_update)
        elif record_list[0] == 'leng_exam':
            self.cur.execute(leng_update)
        self.conn.commit()

db=DB()
db.insert_record(['final_exam', '小明'])