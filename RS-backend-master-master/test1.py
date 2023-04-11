import random

from pandas import DataFrame

from Database import DB

db = DB()
# 随机选题功能
df_1 = db.get_exam_questions()
k, m = divmod(len(df_1), 30)  # k是商 m是余数 在这里k是5 m是0 30个题目
question_list = []
for i in list(range(30)):  # i就是列表中的元素 0 1 2 3 4
    a = df_1.iloc[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]  # a是矩阵
    b = random.randint(0, 4)  # 5个题目中的一个
    question_list.append(a.iloc[b].values.tolist())  # a.iloc[b]查找a矩阵里的第b行
# print(question_list)
df1 = DataFrame(question_list)
# print(df1)
j = 1
for i in range(len(question_list)):
    question_list[i][0] = j
    j += 1
# print(question_list)
df = DataFrame(question_list)
# print(df)
data_list = [tuple(row) for row in df.values]  # 将dataframe读取的数据转化为元祖
# print(data_list)
# print(len(data_list))
n = random.randint(4, 6)  # 生成知识点的数量
# print(n)
question_num = random.sample(range(1, 7), n)  # 确定n个知识点是6个知识点中的哪几个知识点
question_num.sort()  # 对数量进行从小到大排序
print(question_num)
test = []
test1 = []
for i in question_num:
    test.extend(data_list[(i - 1) * 5:i * 5])  # 列表合并
print(test)
print(len(test))
while test:
    test1.extend(random.sample(test[:5], 4))
    test = test[5:]  # 列表截断
result1 = sorted(test1)
# return result1
print(result1)
print(len(result1))
# print(df)
# index = 0
# all_list = []
# for i in range(0, len(df[0])):
#     data = {}
#     option = {}
#     data['question'] = str(df.iloc[index][3])
#     option['A'] = str(df.iloc[index][4])[2:]
#     option['B'] = str(df.iloc[index][5])[2:]
#     option['C'] = str(df.iloc[index][6])[2:]
#     option['D'] = str(df.iloc[index][7])[2:]
#     data['option'] = option
#     data['true'] = str(df.iloc[index][8])
#     data['type'] = 1
#     data['scores'] = str(int(df.iloc[index][2]) + 1)
#     data['checked'] = False
#     all_list.append(data)
#     index += 1
# print(all_list)
user_re2: [0.3267146243734693, 0.41988133551962115, 0.3044203545898332, 0.37464821325774134,
           0.36609875089095534, 0.430948170221083, 0.40581068765095507, 0.39284545089455314]
rec_list: [2, 3, 2, 4, 4, 3, 3, 4]
ques_list2: [(22,), (21,)]
ques_list2: [(38,), (37,), (39,)]
ques_list2: [(70,), (68,)]
ques_list2: [(88,), (85,), (87,), (80,)]
ques_list2: [(104,), (103,), (114,), (110,)]
ques_list2: [(131,), (139,), (132,)]
ques_list2: [(154,), (159,), (155,)]
ques_list2: [(185,), (186,), (183,), (184,)]
