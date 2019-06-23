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

@ddt
class RegisterTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "register")
    cases = wb.read_column_data(read_column)

    @classmethod
    def setUpClass(cls):

        my_log.info("准备开始执行注册接口的测试......")
        cls.request = HTTPRequest2()
        cls.db = ExecuteMysql()

    @data(*cases)   # 拆包，拆成几个参数
    def test_register(self, case):

        # 筛选用例的请求数据中做了#register__phone#标记的数据
        if "#register_phone#" in case.request_data:
            while True:
                # 生成随机号码
                mobile_phone = rand_phone()
                # 查询数据库有无该随机号码
                count = self.db.find_count("SELECT Id FROM member WHERE MobilePhone={}".format(mobile_phone))
                # 数据库中无此随机号码，就不用继续随机生成，直接使用该随机号码
                if count == 0:
                    break
            # 将用例中的#register__phone#替换成随机生成的手机号码
            case.request_data = case.request_data.replace("#register_phone#", mobile_phone)

        # 选取请求的电话号为已注册的测试用例数据
        elif "#exists_phone#" in case.request_data:
            # 从数据库获取第一条号码，给用例参数
            mobile_phone = self.db.find_one("SELECT MobilePhone FROM member LIMIT 1")[0]
            # 用从数据库获取的号码替换掉请求数据中的标记#exists_phone
            case.request_data = case.request_data.replace("#exists_phone#", mobile_phone)

        elif "#login_phone#" in case.request_data:
            # 将登录手机号从配置文件中读取并替换掉用例中的#login_phone#
            case.request_data = case.request_data.replace("#login_phone#", conf.get("test_data", "mobile_phone"))

        elif "#pwd#" in case.request_data:
            # 将登录密码从配置文件中读取并替换掉用例中的#login_phone#
            case.request_data.replace("#pwd#", conf.get("test_data", "pwd"))

        elif "#less_phone" in case.request_data:
            mobile_phone = self.db.find_one("SELECT MobilePhone FROM member WHERE LeaveAmount<500000")

        # 拼接url地址
        url = conf.get("env", "url") + case.url
        self.row = case.case_id + 1
        response = self.request.request(method=case.method, url=url, data=eval(case.request_data))

        # 该打印的内容会显示在报告中
        print("请求数据--> {}".format(case.request_data))
        print("期望结果---> {}".format(case.expected_data))
        print("服务器响应数据--> {}".format(response.json()))

        print(case.request_data, type(case.request_data))
        print(conf.get("test_data", "mobile_phone"), type(conf.get("test_data", "mobile_phone")))

        res = response.json()

        try:
            self.assertEqual(eval(case.expected_data), res)
        except AssertionError as e:
            result = 'FAIL'
            my_log.exception(e)     # 将异常信息记录到日志
            raise e
        else:
            result = 'PASS'
            my_log.debug("预期结果：%s, 实际结果：%s, 测试通过" % (eval(case.expected_data), res))
        finally:
            self.wb.write_data(row=self.row, column=9, msg=result)

    @classmethod
    def tearDownClass(cls):

        my_log.info("注册接口测试执行完毕......")
        cls.request.close()
