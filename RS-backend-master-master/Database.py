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

    # 获取Question的部分题目
    def get_questions(self):
        sql = 'select * from Questions ORDER BY No'  # select 可以使用"*"查找表中所有字段的数据，语法格式如下：select * from 表名;
        # 把sql查询Questions的结果读取为数据框
        result = pd.read_sql(sql, self.conn)
        data_list = [tuple(row) for row in result.values]  # 将pandas读取的数据转化为元祖
        # print(result)
        # print(data_list)
        # print(len(data_list))
        n = random.randint(6, 7)  # 生成知识点的数量
        question_num = random.sample(range(1, 9), n)  # 确定n个知识点是10个知识点中的哪几个知识点
        question_num.sort()  # 对数量进行从小到大排序
        # print(question_num)
        test = []
        test1 = []
        for i in question_num:
            test.extend(data_list[(i - 1) * 5:i * 5])  # 列表合并
        # print(test)
        # print(len(test))
        while test:
            test1.extend(random.sample(test[:5], random.randint(4, 5)))
            test = test[5:]  # 列表截断
        result1 = sorted(test1)
        return result1

    # 获取Examination的所有题目
    def get_exam_questions(self):
        sql = 'select * from Examination'  # select 可以使用"*"查找表中所有字段的数据，语法格式如下：select * from 表名;
        df_1 = pd.read_sql(sql, self.conn)
        # 随机选题功能
        k, m = divmod(len(df_1), 40)  # k是商 m是余数 在这里k是5 m是0 30个题目
        question_list = []
        for i in list(range(40)):  # i就是列表中的元素 0 1 2 3 4
            a = df_1.iloc[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]  # a是矩阵
            b = random.randint(0, 4)  # 5个题目中的一个
            question_list.append(a.iloc[b].values.tolist())  # a.iloc[b]查找a矩阵里的第b行
        df1 = DataFrame(question_list)
        print(df1)
        j = 1
        for i in range(len(question_list)):
            question_list[i][0] = j
            j += 1
        print(question_list)
        df = DataFrame(question_list)
        print(df)
        data_list = [tuple(row) for row in df.values]  # 将dataframe读取的数据转化为元祖
        print(data_list)
        print(len(data_list))
        n = random.randint(6, 7)  # 生成知识点的数量
        print(n)
        question_num = random.sample(range(1, 9), n)  # 确定n个知识点是6个知识点中的哪几个知识点
        question_num.sort()  # 对数量进行从小到大排序
        print(question_num)
        test = []
        test1 = []
        for i in question_num:
            test.extend(data_list[(i - 1) * 5:i * 5])  # 列表合并
        print(test)
        print(len(test))
        while test:
            test1.extend(random.sample(test[:5], random.randint(4, 5)))
            test = test[5:]  # 列表截断
        result1 = sorted(test1)
        print(len(result1))
        return result1

    # 判断用户是否存在
    def judge_user(self, user, pas):  # 传入的参数是用户输入的姓名user和密码pas
        sql_user = "SELECT username FROM user"  # 从数据库中查找所有的username
        sql_pass = "SELECT pass FROM user WHERE username = %s"  # 查找user用户的密码
        # 开启游标功能执行这个SQL语句后，系统并不会将结果直接打印到屏幕上，而是将上述得到的结果，找个地方存储起来，提供一个游标接口给我们，当你需要获取数据
        # 的时候，就可以从中拿数据。
        self.cur.execute(sql_user)
        user_db = self.cur.fetchall()  # 获取数据库中username这一列的所有名字
        for i in user_db:  # 为user_db去掉一层括号（因为返回的对象是元组）
            if user == i[0]:  # 再去掉一层括号，得到数据库中的username字符串和输入的user比对
                self.cur.execute(sql_pass, user)
                pass_db = self.cur.fetchone()[0]  # 此时,通过 pass_db[0],pass_db[1]可以依次访问sql_pass,user
                if pas == pass_db:  # pass_db即是sql_pass
                    return 0  # 有该用户且密码正确
                else:
                    return 1  # 有该用户，密码错误
        return -1  # 无该用户

    # 获取用户的做题情况,传入参数是user的名字
    def get_user_last_result(self, user):
        sql_user = "SELECT 第1题,第2题,第3题,第4题,第5题,第6题,第7题,第8题,第9题,第10题,第11题,第12题,第13题,第14题,第15题,第16题,第17题,第18题,第19题,第20题,第21题,第22题,第23题,第24题,第25题,第26题,第27题,第28题,第29题,第30题,第31题,第32题,第33题,第34题,第35题,第36题,第37题,第38题,第39题,第40题 FROM user WHERE username = %s"
        self.cur.execute(sql_user, user)
        return self.cur.fetchone()  # 此时,返回的是输入用户对应的id

    # 获取用户的id，传入参数user的名字
    def get_userid(self, user):
        sql_userid = "SELECT id FROM user WHERE username = %s"
        self.cur.execute(sql_userid, user)
        return self.cur.fetchone()[0]  # 此时,返回的是输入用户对应的id

    # 在最后一行后面插入最新的用户，返回的最新用户的id
    def insert_user(self, username, userpass):
        # order by id asc是按id进行降序排列，limit 0,1 是只取记录中的第一条.所以这条语句只能得到一条记录如想取前10条则 limit 0,10或limit 10如想取第10至20条则 limit 10,20
        self.cur = self.conn.cursor()  # 先建立一个游标对象
        sql_search_no = "select * from user order by id desc limit 0,1"  # 将数据库id这一列按降序排列，每次只取第一个数据
        try:
            self.cur.execute(sql_search_no)
            last_no = self.cur.fetchone()[0]  # 获取数据库中最后一个id号
            user_id = int(last_no) + 1
        except:
            user_id = 1222
        # sql = "INSERT INTO user VALUES (%r , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        sql = "INSERT INTO user(id, username, pass) VALUES (%r , %s, %s)"  # 创建新用户
        ques_sql = "INSERT INTO record VALUES (%s , 0, 0,0,0)" % username
        user_list = [int(user_id), username, userpass]
        try:
            self.cur.execute(sql, user_list)  # 执行数据库插入
            self.cur.execute(ques_sql)  # 执行数据库插入
            self.conn.commit()  # 提交
        except:
            print("插入新用户失败")
        return user_id

    # 插入用户的做题结果
    def insert_result(self, ins_list):
        # 使用cursor()方法创建一个游标对象
        self.cur = self.conn.cursor()  # 先建立一个游标对象
        # sql_insert = "INSERT INTO user VALUES (%r,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_update = "update user set 第1题 = %s, 第2题 = %s, 第3题 = %s, 第4题 = %s,第5题 = %s, 第6题 = %s,第7题 = %s, 第8题 = %s,第9题 = %s, 第10题 = %s,第11题 = %s, 第12题 = %s,第13题 = %s, 第14题 = %s,第15题 = %s, 第16题 = %s,第17题 = %s, 第18题 = %s,第19题 = %s, 第20题 = %s,第21题 = %s,第22题 = %s, 第23题 = %s ,第24题 = %s, 第25题 = %s,第26题 = %s, 第27题 = %s ,第28题 = %s, 第29题 = %s, 第30题 = %s,第31题 = %s, 第32题 = %s ,第33题 = %s, 第34题 = %s, 第35题 = %s,第36题 = %s, 第37题 = %s ,第38题 = %s, 第39题 = %s, 第40题 = %s where username = %s"
        try:
            self.cur.execute(sql_update, ins_list)
            self.conn.commit()
            print("插入成绩成功")
        except:
            print("插入成绩失败")

    def choose_questing_level(self, level, rand_id):  # 选择问题的难度
        sql_choose = "SELECT NO,question,A,B,C,D,CorrectAnswer FROM Questions WHERE 'Difficulty Level' = %s LIMIT %s,1" % (
            level, rand_id)  # 查找user用户的密码
        self.cur.execute(sql_choose)
        ans = self.cur.fetchone()
        return ans[0], ans[1], ans[2], ans[3], ans[4], ans[5], ans[6]

    def get_user_result(self):  # 得到用户的做题结果，包括做对做错和是否做过
        # sql 命令
        sql = 'select * from user'
        self.cur.execute(sql)
        list1 = []  # list1是ph,成绩：做对，没做过，做错
        list2 = []  # list2是r,是否做过
        while True:
            row = self.cur.fetchone()
            if not row:
                break
            a = row[3:]
            list1.append(list(a))
            list2.append(list(a))

        for i in range(len(list1)):
            for j in range(len(list1[i])):
                if list1[i][j] != '-1':
                    list2[i][j] = 1
                else:
                    list2[i][j] = 0
        score = list(map(list, zip(*list1)))  # 转置矩阵的行和列
        have_done = list(map(list, zip(*list2)))
        return score, have_done

    def get_user_num(self):  # 获取用户数和题目数
        user_result, _ = self.get_user_result()
        ques_num = len(user_result)
        user_num = len(user_result[0])
        # print('ques_num',ques_num)
        # print('user_num',user_num)
        return int(ques_num), int(user_num)

    # 选取一个知识点某一个难度等级的5道题
    def rec_question(self, knowledge, level):
        sql_ques = "SELECT Question, A, B, C, D, CorrectAnswer,Difficulty_Level FROM Recommendation WHERE Difficulty_Level = %s order by No" % level
        # sql_ques = "SELECT No FROM Recommendation WHERE Difficulty_Level = %s order by No" % level
        self.cur.execute(sql_ques)
        ques = self.cur.fetchall()  # 将同一难度的5个知识点存入ques列表
        # print(ques)
        # n = random.randint(1, int(len(ques)/5))  # 生成的随机数n: 1 <= n <= 2
        return ques[int(len(ques) / 8) * knowledge:int(len(ques) / 8) * knowledge + 5]

    # 冷启动求均值
    def leng_mu(self):
        mu_list = []
        score_list, _ = self.get_user_result()
        print('score_list', score_list)
        for i in score_list:
            total = 0.0
            for ele in range(0, len(i) - 1):  # 不计算新增用户的值
                total = total + float(i[ele])
            mu_list.append(total / (len(i) - 1))
        return mu_list  # user表中已有用户对25道题目的成绩的均值

    def insert_record(self, record_list):
        # 使用cursor()方法创建一个游标对象
        print(record_list)
        self.cur = self.conn.cursor()  # 先建立一个游标对象
        final_update = "update record set final_exam = 1 where username = '"+record_list[1]+"'"
        exam_update = "update record set exam = 1 where username = '"+record_list[1]+"'"
        recommend_update = "update record set recommend = 1 where username = '"+record_list[1]+"'"
        leng_update = "update record set leng_exam = 1 where username = '"+record_list[1]+"'"
        if record_list[0] == 'final_exam':
            self.cur.execute(final_update)
        elif record_list[0] == 'exam_exam':
            self.cur.execute(exam_update)
        elif record_list[0] == 'recommend':
            self.cur.execute(recommend_update)
        elif record_list[0] == 'leng_exam':
            self.cur.execute(leng_update)
        self.conn.commit()
        print("插入记录成功")

    def judge_final(self, username):  # 判断是冷启动还是推荐功能
        print("开始查询"+username)
        sql = "SELECT leng_exam,recommend FROM record WHERE username =%s"   # 从数据库中查找所有的username
        self.cur.execute(sql,username)
        ex_result = self.cur.fetchone()
        print(ex_result)
        if ex_result[0] == '1' or ex_result[1] == '1':
            return 1
        else:
            return 0

    def insert_logs(self, ins_list):  # 插入日志表，参数是用户名，日期，模式名，分数
        score_sql = "INSERT INTO logs VALUES (%s,%s,%s,%s)"
        self.cur.execute(score_sql, ins_list)
        self.conn.commit()
#
db=DB()
db.get_user_result()
db.insert_record(['exam','3'])

