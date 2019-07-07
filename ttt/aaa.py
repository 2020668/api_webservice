# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/24

E-mail:keen2020@outlook.com

=================================


"""


# class ConText(object):
#     pass
#
#
# # 设置属性
# # setattr(ConText, "name", "musen")
#
#
# setattr(ConText, "name", 111)
#
#
# def replace(data):
#     value = getattr(ConText, "name")
#     data = data.replace("a", value)
#     return data
#     # print(getattr(ConText, "name"))
#
#
# data = "ghshgdhga"
# res = replace(data)
# print(res)
# # replace()

# 匹配字符串中特定字符后的数字，如匹配phone后的130
import re

s = '{"verify_code":"#mcode#", "user_id":"baozi","channel_id":"1","pwd":"123456", "mobile":"#phone130#","ip":"1.1.1.1"}'
reg = r'phone(.{3})'
ri = re.compile(reg)
res = re.findall(ri, s)
print(res[0])
