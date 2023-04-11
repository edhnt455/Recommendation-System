import random
import os
import numpy as np
# import matplotlib.pyplot as plt
import tensorflow as tf
# from app_global import appGlobal as ag
from Database import DB

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def rec_question_num(result):
    def sum_list(list1):
        total = 0
        for ele in range(0, len(list1)):
            total = total + list1[ele]
        return total

    list_n = []  # 分配后的整数数组
    total_result = sum_list(result)
    list_k1 = []  # 实际占比K
    for i in result:
        list_n.append(int(i / total_result * 25))
        list_k1.append(i / total_result)

    n = 25- sum_list(list_n)
    list_k2 = []  # 预期占比K'
    for i in list_n:
        list_k2.append(i / 25)

    list_k3 = []  # 实际与预期的差值
    for i in range(len(list_k1)):
        list_k3.append(list_k1[i] - list_k2[i])
    sorted_id = sorted(range(len(list_k3)), key=lambda k: list_k3[k])

    list_t = list_k3
    for i in range(len(list_k3)):
        if i < n:
            list_t[sorted_id[i]] = 1
        else:
            list_t[sorted_id[i]] = 0
    list_b = []  # 最后分配结果
    for i in range(len(list_n)):
        list_b.append(list_t[i] + list_n[i])
    return list_b


class PqlEngine:
    def __init__(self, db, id):
        self.db = db  # db:表示数据库名称，也就是questions，传递给DB()的实例化对象database
        print('initialize personalized question lib engine')
        self.nm, self.nu = db.get_user_num()  # 题目总数,学生总数
        self.n = int(self.nm / 5)  # 知识点数量
        self.lanmeda = 0.1  # L2调整项系数
        self.epochs = 6000  # 训练遍数
        self.result = []
        self.id = id
        self.question_list = []
        # print("题数")
        # print(self.nm)
        # print(self.nu)

    def load_dataset(self):
        # ph = np.zeros(shape=(self.nm, self.nu), dtype=np.float32)
        # r = np.ones(shape=(self.nm, self.nu), dtype=np.int32)
        result_list1, result_list2 = self.db.get_user_result()
        ph = np.array(result_list1, dtype=np.float32)  # 用户的成绩
        r = np.array(result_list2, dtype=np.int32)  # 用户是否做过题目，1代表做过，0代表没做过
        # print(ph)
        # print('r', r)
        # 求出mu（因为仅统计大于等于零项，所以不能用tf.reduce_mean函数）
        mu = np.zeros(shape=(self.nm, 1))
        for row in range(self.nm):
            sum = 0.0
            num = 0.0
            for col in range(self.nu):
                if 1 == r[row][col]:
                    sum += ph[row][col]  # 每个题目所有学生得分总和
                    num += 1  # 统计每个题目做过学生的人数
            # print('sum', sum)
            # print('num', num)
            mu[row][0] = sum / num
        print(mu)
        self.refine_ph(ph, mu)
        # print(ph)
        ph = ph - mu
        # print(ph)
        return ph, r, mu

    def refine_ph(self, ph, mu):
        for row in range(self.nm):
            for col in range(self.nu):
                if ph[row][col] < 0.0:  # 将所有学生未做过的题目，全部设置为相应的均值
                    ph[row][col] = mu[row][0]

    def calDeltaY(self, Y, Y_):
        sum = 0.0
        for row in range(self.nm):
            for col in range(self.nu):
                if 1 == self.r[row][col]:
                    sum += (Y[row][col] - Y_[row][col]) * (Y[row][col] - Y_[row][col])
        return sum

    def build_model(self):
        print('build model')
        self.Y_ = tf.compat.v1.placeholder(shape=[self.nm, self.nu], dtype=tf.float32, name='Y_')

        self.X = tf.Variable(tf.random.truncated_normal(shape=[self.nm, self.n], mean=0.0, stddev=0.01, seed=1.0),
                             dtype=tf.float32, name='X')

        self.UT = tf.Variable(tf.random.truncated_normal(shape=[self.n, self.nu], mean=0.0, stddev=0.01, seed=1.0),
                              dtype=tf.float32, name='UT')

        self.Y = tf.matmul(self.X, self.UT)

        self.L = self.calDeltaY(self.Y, self.Y_)  # tf.reduce_sum((self.Y - self.Y_)*(self.Y - self.Y_))
        self.J = self.L + self.lanmeda * tf.reduce_sum(self.X ** 2) + self.lanmeda * tf.reduce_sum(self.UT ** 2)
        self.train_step = tf.compat.v1.train.AdamOptimizer(learning_rate=0.001, beta1=0.9,
                                                           beta2=0.999, epsilon=1e-08, use_locking=False,
                                                           name='Adam').minimize(self.J)

    def train(self):
        self.build_model()
        with tf.compat.v1.Session() as sess:
            sess.run(tf.compat.v1.global_variables_initializer())
            for epoch in range(self.epochs):
                X, UT, Y, J, train_step = sess.run([self.X, self.UT, self.Y, self.J, self.train_step],
                                                   feed_dict={self.Y_: self.Y_ph})

            self.Xv = X
            self.UTv = UT
            print('self.Xv',self.Xv)
            print('self.UTv',self.UTv)

    def predict(self):
        Uv = np.transpose(self.UTv)

        for row in range(self.nm):
            for col in range(self.nu):
                # np.dot为矩阵乘积，得出每道题目训练计算出的分数
                self.result.append(np.dot(self.Xv[row], Uv[col]) + self.mu[row][0])
        print('self.result:', self.result)
        user_re = []  # 指定用户的30道题目的训练出的分数
        user_re2 = []  # 用户每个知识点的需求度
        # self.result)防止最后一个取不到
        for i in range(self.id, len(self.result) , self.nu):  # id到题目总数，每次增加学生个数，例如输出1,6,11等数字
            user_re.append(self.result[i])
        print('user_re:', user_re)
        print(len(user_re))
        # print(user_re)
        # print(len(user_re))
        while user_re:
            num_sum = sum(user_re[:5])
            # print(num_sum)
            # num_sum / 5 / 6 + 0.5:/5是为了求平均值，/6是因为需求度区间6内，2-是为了取到正数，用1-会出现负数，不利于分配题目
            user_re2.append((1 - (num_sum / 5 / 15 + 0.5)))  # 每个知识点的需求程度（5个题目一个知识点），每种知识点共15分，数值越大需求越大
            user_re = user_re[5:]  # 列表截断
        rec_list = rec_question_num(user_re2)
        print('user_re2:', user_re2)
        print(len(user_re2))
        print('rec_list:', rec_list)  #各个知识点需求量
        list_ques = self.recommand_ques(rec_list)
        print('list_ques',list_ques)
        return list_ques

    def rand_ques(self, diff, ques_num, kno):  # 输入为难度等级，需求数量，知识点，输出为该知识点的需求题目
        ques_list = []
        ques_list2 = []
        if diff == 1:
            list_1 = [1, 2, 3]  # 题目的难度等级为1,2,3
        else:
            list_1 = [4, 5]  # 题目的难度等级为4,5
        for i in list_1:
            ques_list += self.db.rec_question(kno, i)  # 根据题目难度和知识点推荐题目存入ques_list,for循环遍历一次是5道题目
        # print('ques_list',ques_list)
        # print(len(ques_list))
        k = random.sample(range(0, len(ques_list) - 1), ques_num)  # 从ques_list中随机取到5个题目的序号
        for i in k:
            ques_list2.append(ques_list[i])
        print('ques_list2',ques_list2)
        return ques_list2  # 根据题目的序号返回随机到的题目

    def recommand_ques(self, rec_list):  # 根据需求量推荐题目
        for i in range(len(rec_list)):  # 0-4
            if rec_list[i] <= 2:
                self.question_list += self.rand_ques(2, rec_list[i], i)
            else:
                self.question_list += self.rand_ques(1, rec_list[i], i)
        return self.question_list

    def run(self):
        self.Y_ph, self.r, self.mu = self.load_dataset()
        self.train()
        return self.predict()


# db = DB()
# test = PqlEngine(db,6)
# a = test.run()
# print(a)
