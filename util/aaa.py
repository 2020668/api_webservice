# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/14

E-mail:keen2020@outlook.com

=================================


"""


import unittest
from library.ddt import ddt, data
from common.read_excel import ReadExcel
from common.logger import my_log   # 可直接导入对象
from common.config import conf
import os
from common.constant import DATA_DIR
from common.http_request import HTTPRequest2
import random
from common.execute_mysql import ExecuteMysql


# 从配置文件获取数据
file_name = conf.get('excel', 'file_name')
read_column = conf.get('excel', 'read_column')
read_column = eval(read_column)     # 将str转换成list


def rand_phone():
    phone = "133"
    for i in range(8):
        phone_end = random.randint(0, 9)
        phone += str(phone_end)
    return phone


wb = ReadExcel(os.path.join(DATA_DIR, file_name), "register")
cases = wb.read_column_data(read_column)


my_log.info("准备开始执行注册接口的测试......")
request = HTTPRequest2()
db = ExecuteMysql()


def test(case):

    # 筛选用例的请求数据中做了#register__phone#标记的数据
    if "#register_phone#" in case.request_data:
        while True:
            # 生成随机号码
            mobile_phone = rand_phone()
            # 查询数据库有无该随机号码
            count = db.find_count("SELECT * FROM member WHERE MobilePhone={}".format(mobile_phone))
            # 数据库中无此随机号码，就不用继续随机生成，直接使用该随机号码
            if count == 0:
                break
        # 将用例中的#register__phone#替换成随机生成的手机号码
        print(mobile_phone, type(mobile_phone))
        print(case.request_data, type(case.request_data))
        # case.request_data.replace("#register_phone#", mobile_phone)
        case.request_data.replace("#register_phone#", mobile_phone)
        print(case.request_data)


if __name__ == '__main__':
    for case in cases:
        test(case)


