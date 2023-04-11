import json
import random
from pandas import DataFrame
from flask import request, jsonify, Blueprint
from flask import session
from Database import DB
from tens import PqlEngine

user = Blueprint("user", __name__)  # 用户蓝图对象
db = DB()  # 实例化的数据库
glo_username = ''


# 用户注册
@user.route("/register", methods=["POST"])
def user_register():
    req_data = request.get_json()
    nn = req_data.get("username")  # 获取账号
    np = req_data.get("password")  # 获取密码
    result_list = []
    for i in range(40):  # 将所有题目结果先预置为0
        result_list.append(-1)
    result = db.judge_user(nn, np)  # 调用数据库类中的函数,根据result的结果判断用户是否存在
    if result == 0 or result == 1:  # 用户注册过并且密码正确
        return jsonify(code=405, msg="用户名已存在")
    else:
        try:
            db.insert_user(nn, np)
            result_list.append(nn)
            db.insert_result(result_list)  # 初始化结果列表为0
            return jsonify(code=200, msg="用户注册成功")
        except Exception as e:
            print(e)
            return jsonify(code=400, msg="注册失败")


# 用户登录
@user.route("/login", methods=["POST"])
def user_login():
    req_data = request.get_json()
    check_name = req_data.get("username")  # 获取账号
    check_password = req_data.get("password")  # 获取密码
    session["user_name"] = check_name
    session["user_password"] = check_password
    ans = db.judge_user(check_name, check_password)
    if ans == 0:
        global glo_username
        glo_username = check_name
        last_result1 = db.get_user_last_result(check_name)
        last_result = 0
        for i in last_result1:
            last_result += int(float(i))  # 对字符列表求和（负数）
        # print(last_result1)
        # last_result = sum([int(each_e) for each_e in last_result1])  # 对字符列表求和（负数）
        # print(last_result)
        if last_result != -40:  # 判断用户有没有做过题库
            return jsonify(code=200, msg="跳转到推荐界面")
        else:
            return jsonify(code=300, msg="摸底或者冷启动")
    elif ans == 1:
        return jsonify(code=400, msg="账号或者密码错误")
    else:
        return jsonify(code=500, msg="跳转到注册界面")


# libs界面
@user.route("/libs", methods=["POST"])
def libs():
    global glo_username
    last_result1 = db.get_user_last_result(glo_username)
    last_result=0
    for i in last_result1:
        last_result += int(float(i))# 对字符列表求和（负数）
    # last_result = sum([each_e for each_e in last_result1])  # 对字符列表求和（负数）
    if last_result != -40:  # 判断用户有没有做过题库
        return jsonify(code=200, msg="跳转到推荐界面")
    else:
        return jsonify(code=300, msg="摸底或者冷启动")


# 最终测试
@user.route("/final_exam", methods=["POST"])
def final_exam():
    # 随机选题功能
    df = db.get_exam_questions()
    ques_id = []
    ques = []
    total_score = 0
    total_score1 = []
    # 将所有题目添加到列表中
    for index in range(0, len(df)):
        data = {}
        option = {}
        ques_id.append(str(df[index][0]))
        data['question'] = str(df[index][3])
        option['A'] = str(df[index][4])[2:]
        option['B'] = str(df[index][5])[2:]
        option['C'] = str(df[index][6])[2:]
        option['D'] = str(df[index][7])[2:]
        data['option'] = option
        data['true'] = str(df[index][8])
        data['type'] = 1
        data['scores'] = str(df[index][2])
        total_score1.append(str(df[index][2]))
        data['checked'] = False
        ques.append(data)
    print(total_score1)
    for ele in range(0, len(total_score1)):
        total_score = total_score + int(total_score1[ele])
    print('total_score', total_score)
    global glo_username
    re = db.judge_final(glo_username)
    result = {'ques_list': ques, 'access': re, 'id': ques_id, 'score': total_score}
    bJson = json.dumps(result, ensure_ascii=False)
    return bJson


# 摸底测试
@user.route("/exam", methods=["POST"])
def user_exam():
    try:
        df = db.get_questions()
        total_score = 0
        total_score1 = []
        ques_id = []
        ques = []
        # 将所有题目添加到列表中
        for index in range(0, len(df)):
            data = {}
            option = {}
            ques_id.append(str(df[index][0]))
            data['question'] = str(df[index][3])
            option['A'] = str(df[index][4])[2:]
            option['B'] = str(df[index][5])[2:]
            option['C'] = str(df[index][6])[2:]
            option['D'] = str(df[index][7])[2:]
            data['option'] = option
            data['true'] = str(df[index][8])
            data['type'] = 1
            data['scores'] = str(df[index][2])
            total_score1.append(str(df[index][2]))
            data['checked'] = False
            ques.append(data)
        print(total_score1)
        for ele in range(0, len(total_score1)):
            total_score = total_score + int(total_score1[ele])
        print('total_score', total_score)
        all_list = {'ques': ques, 'id': ques_id, 'score': total_score}
        bJson = json.dumps(all_list, ensure_ascii=False)
        return bJson
    except(Exception):
        # print(Exception)
        return jsonify(code=400, msg="发生错误")


# 冷启动
@user.route("/leng_exam", methods=["POST"])
def leng_exam():
    req_data = request.get_json()
    username = req_data.get("username")  # 获取用户名
    user_id = db.get_userid(username)
    list_mu = db.leng_mu()
    list_mu.append(username)
    db.insert_result(list_mu)  # 初始化结果列表为0
    test = PqlEngine(db, user_id)
    rec_questions = test.run()
    print('rec_questions', rec_questions)
    index = 0
    ques = []
    total_score = 0
    total_score1 = []
    for i in range(0, len(rec_questions)):
        data = {}
        option = {}
        data['question'] = str(rec_questions[index][0])
        option['A'] = str(rec_questions[index][1])[2:]
        option['B'] = str(rec_questions[index][2])[2:]
        option['C'] = str(rec_questions[index][3])[2:]
        option['D'] = str(rec_questions[index][4])[2:]
        data['option'] = option
        data['true'] = str(rec_questions[index][5])
        data['type'] = 1
        data['scores'] = str(rec_questions[index][6])
        total_score1.append(str(rec_questions[index][6]))
        data['checked'] = False
        ques.append(data)
        index += 1
    print(total_score1)
    for ele in range(0, len(total_score1)):
        total_score = total_score + int(total_score1[ele])
    print('total_score', total_score)
    all_list = {'ques': ques, 'score': total_score}
    bJson = json.dumps(all_list, ensure_ascii=False)
    return bJson


# 推荐
@user.route("/recommend_exam", methods=["POST"])
def rec_exam():
    # req_data = request.get_json()
    global glo_username
    # username = req_data.get("username")  # 获取做题结果
    user_id = db.get_userid(glo_username)
    test = PqlEngine(db, user_id)
    df = test.run()
    print(df)
    index = 0
    ques = []
    all_list = []
    total_score = 0
    total_score1 = []
    # 将所有题目添加到列表中
    for i in range(0, len(df)):
        data = {}
        option = {}
        data['question'] = str(df[index][0])
        option['A'] = str(df[index][1])[2:]
        option['B'] = str(df[index][2])[2:]
        option['C'] = str(df[index][3])[2:]
        option['D'] = str(df[index][4])[2:]
        data['option'] = option
        data['true'] = str(df[index][5])
        data['type'] = 1
        data['scores'] = str(df[index][6])
        total_score1.append(str(df[index][6]))
        data['checked'] = False
        ques.append(data)
        index += 1
    print(total_score1)
    for ele in range(0, len(total_score1)):
        total_score = total_score + int(total_score1[ele])
    print('total_score', total_score)
    all_list = {'ques': ques, 'score': total_score}
    bJson = json.dumps(all_list, ensure_ascii=False)
    return bJson


@user.route("/result", methods=["POST"])
def insert_result():
    init_result = []
    for i in range(40):  # 将所有题目结果先预置为-1
        init_result.append(-1)
    global glo_username
    init_result.append(glo_username)
    req_data = request.get_json()
    result = req_data.get("result")  # 获取做题结果
    result_id = req_data.get("id")
    print('result_id', result_id)
    examname = req_data.get("examname")
    exam_list = [examname, glo_username]
    db.insert_record(exam_list)
    for i in range(len(result_id)):
        init_result[int(result_id[i]) - 1] = result[i]
    for i in range(len(init_result)):
        if init_result[i] == 1:
            if i % 5 == 0:
                init_result[i] = 1
            elif i % 5 == 1:
                init_result[i] = 2
            elif i % 5 == 2:
                init_result[i] = 3
            elif i % 5 == 3:
                init_result[i] = 4
            else:
                init_result[i] = 5
        elif init_result[i] == 0:
            if i % 5 == 0:
                init_result[i] = 0
            elif i % 5 == 1:
                init_result[i] = 0
            elif i % 5 == 2:
                init_result[i] = 0
            elif i % 5 == 3:
                init_result[i] = 0
            else:
                init_result[i] = 0
    print(init_result)
    db.insert_result(init_result)
    return jsonify(code=200, msg="成绩插入成功")
    # except:
    #     return jsonify(code=400, msg="成绩插入失败")


@user.route("/record", methods=["POST"])
def insert_record():
    try:
        req_data = request.get_json()
        username = req_data.get("username")  # 获取用户名
        if req_data.get("is_leng"):  # 获取题目模式
            examname = 'leng_exam'
        else:
            examname = "recommend"
        exam_list = [examname, username]
        db.insert_record(exam_list)
        return jsonify(code=200, msg="成绩插入成功")
    except:
        return jsonify(code=400, msg="成绩插入失败")
