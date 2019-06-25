# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/15

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
from common.execute_mysql import ExecuteMysql
from common.tools import data_replace
# from common.tools import read
from common.tools import ConText

# 从配置文件获取数据
file_name = conf.get('excel', 'file_name')
read_column = conf.get('excel', 'read_column')
read_column = eval(read_column)     # 将str转换成list


@ddt
class AuditTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "audit")
    cases = wb.read_column_data(read_column)

    @classmethod
    def setUpClass(cls):

        my_log.info("准备开始执行审核接口的测试......")
        cls.request = HTTPRequest2()
        cls.db = ExecuteMysql()

    @data(*cases)   # 拆包，拆成几个参数
    def test_audit(self, case):

        if "#login_phone#" in case.request_data:
            # 将登录手机号从配置文件中读取并替换掉用例中的#login_phone#
            case.request_data = data_replace(case.request_data)

        if "#pwd#" in case.request_data:
            # 将登录密码从配置文件中读取并替换掉用例中的#login_phone#
            case.request_data = data_replace(case.request_data)

        if "#memberid#" in case.request_data:
            # 将登录密码从配置文件中读取并替换掉用例中的#login_phone#
            case.request_data = data_replace(case.request_data)

        if case.check_mysql:
            # 替换sql语句中的memberid
            case.check_mysql = data_replace(case.check_mysql)
            # 查询该memberid刚刚加标的loanid
            loanid = self.db.find_one(case.check_mysql)[0]
            # 将loanid赋给ConText类的key属性
            setattr(ConText, "key", str(loanid))

        if "#loanid#" in case.request_data:
            case.request_data = data_replace(case.request_data)

        # 拼接url地址，发送请求
        url = conf.get("env", "url") + case.url
        self.row = case.case_id + 1
        response = self.request.request(method=case.method, url=url, data=eval(case.request_data))  # 将str转换成dict
        # 该打印的内容会显示在报告中
        print("请求数据--> {}".format(case.request_data))
        print("期望结果---> {}".format(case.expected_data))
        print("服务器响应数据--> {}".format(response.json()))

        try:
            # res = response.json()返回json格式，自动转换成Python的dict类型，只取部分字段进行断言
            res = {"status": response.json()["status"], "code": response.json()["code"]}
            self.assertEqual(eval(case.expected_data), res)

        except AssertionError as e:
            result = 'FAIL'
            my_log.exception(e)     # 将异常信息记录到日志
            raise e
        else:
            result = 'PASS'
            my_log.debug("预期结果：%s, 实际结果：%s, 测试通过" % (eval(case.expected_data), res))

        finally:
            self.wb.write_data(row=self.row, column=10, msg=result)

    @classmethod
    def tearDownClass(cls):

        my_log.info("审核接口测试执行完毕......")
        cls.request.close()
        cls.db.close()
