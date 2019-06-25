# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/24

E-mail:keen2020@outlook.com

=================================


"""


class ConText(object):
    pass


# 设置属性
# setattr(ConText, "name", "musen")


setattr(ConText, "name", 111)


def replace(data):
    value = getattr(ConText, "name")
    data = data.replace("a", value)
    return data
    # print(getattr(ConText, "name"))


data = "ghshgdhga"
res = replace(data)
print(res)
# replace()

