# class Solution(object):
#     def two_sum(self, nums, target):
#         """这样写更直观，遍历列表同时查字典"""
#         #将遍历的元素存入一个字典
#         dct = {}
#         # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，
#         # 同时列出数据和数据下标，一般用在 for 循环当中。
#         for i, n in enumerate(nums):#字典查询，字典名[键值]=value值
#             cp = target - n
#             if cp in dct:
#                 return [dct[cp], i]
#             else:
#                 dct[n] = i
#
#
# solution = Solution()
# a = solution.two_sum([1, 2, 3, 4], 7)
# print(a)


import numpy
a=numpy.random.randn(3,4).shape

print(a)





