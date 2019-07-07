# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/25

E-mail:keen2020@outlook.com

=================================


"""

import re
from common.config import conf
import random

# 匹配任意字符，至少一次，关闭贪婪
p = r"#(.+?)#"


class ConText(object):
    pass


# def read(data):
#     setattr(ConText, "key", data)

def rand_phone(segment):
    phone = str(segment)
    for i in range(8):
        phone_end = random.randint(0, 9)
        phone += str(phone_end)
    return phone


def data_replace(data):
    """
    :param data: 用例的参数
    :return: 替换之后的结果
    """
    while re.search(p, data):
        key = re.search(p, data).group(1)
        try:
            value = conf.get("test_data", key)
        except:
            # value = getattr(ConText, "loanid")
            if "loanid" in data:
                value = getattr(ConText, "loanid")
            if "phone1" in data:
                value = rand_phone(eval(data)["mobile"][6:9])
        data = re.sub(p, value, data, count=1)
    return data


if __name__ == '__main__':
    # data = "hasdgiioghgaoigh#mobile_phone#shg;g#pwd#"
    # res = data_replace(data)
    # print(res)
    # phone = rand_phone(133)
    # print(phone)
    # data = "#phone133#"
    # data = data_replace(data)
    # print(data)
    data = "{'client_ip':'1.1.1.1', 'tmpl_id':'1', 'mobile':'#phone130#'}"
    # # data = data_replace(data)
    # # print(data)
    # res = eval(data)["mobile"]
    res = data_replace(data)
    print(res)
    print(type(res))
