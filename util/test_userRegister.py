# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/7/3

E-mail:keen2020@outlook.com

=================================


"""


import unittest
from library.ddt import ddt, data
from custom.read_excel import ReadExcel
from custom.logger import my_log   # 可直接导入对象
from custom.config import conf
import os
from custom.constant import DATA_DIR
from custom.http_request import HTTPRequest2
from custom.execute_mysql import ExecuteMysql
from custom.tools import data_replace, rand_name, rand_ip
from custom.web_request import WebRequests


# 从配置文件获取数据
file_name = conf.get('excel', 'file_name')
read_column = conf.get('excel', 'read_column')
read_column = eval(read_column)     # 将str转换成list


@ddt
class UserRegisterTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "userRegister")
    # wb = ReadExcel(os.path.join(DATA_DIR, file_name), "re")
    cases = wb.read_column_data(read_column)

    @classmethod
    def setUpClass(cls):

        my_log.info("======准备开始执行注册接口的测试======")
        cls.request = HTTPRequest2()
        cls.db = ExecuteMysql()

    @classmethod
    def tearDownClass(cls):

        my_log.info("======注册接口测试执行完毕======")
        cls.request.close()
        cls.db.close()

    # 自动获取验证码
    def m_code(self, ip, mobile):
        data = {'client_ip': ip, 'tmpl_id': '1', 'mobile': mobile}
        url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
        webs = WebRequests()
        response = webs.web_request(url=url, interface="sendMCode", data=data)
        sql = "SELECT Fverify_code FROM sms_db_{}.t_mvcode_info_{} WHERE Fmobile_no={}". \
            format(mobile[9:11], mobile[8], mobile)
        mcode = self.db.find_one(sql)[0]
        return mcode

    @data(*cases)   # 拆包，拆成几个参数
    def test_user_register(self, case):

        # 替换成随机手机号
        case.request_data = data_replace(case.request_data)
        # 替换ip
        case.request_data = case.request_data.replace('$ip', rand_ip())
        # 获取验证码
        mcode = self.m_code(ip=eval(case.request_data)['ip'], mobile=eval(case.request_data)['mobile'])
        # 替换验证码
        case.request_data = case.request_data.replace('mcode', mcode)

        if "name" in case.request_data:
            case.request_data = case.request_data.replace("name", rand_name())

        else:
            case.request_data = data_replace(case.request_data)

        # 拼接url地址
        url = conf.get("env", "url") + case.url
        self.row = case.case_id + 1
        webs = WebRequests()
        response = webs.web_request(url=url, interface='userRegister', data=case.request_data)

        # 该打印的内容会显示在报告中
        print("请求参数--> {}".format(case.request_data))
        my_log.info("请求参数--> {}".format(case.request_data))

        print("期望结果--> {}".format(case.expected_data))
        my_log.info("期望结果--> {}".format(case.expected_data))

        print("服务器响应数据--> {}".format(response))
        my_log.info("服务器响应数据--> {}".format(response))

        try:
            self.assertEqual(eval(case.expected_data), response)

        except AssertionError as e:
            result = 'FAIL'
            my_log.exception(e)     # 将异常信息记录到日志
            raise e
        else:
            result = 'PASS'
            my_log.info("断言结果:{}, 测试通过".format(result))

        finally:
            self.wb.write_data(row=self.row, column=8, msg=str(response))
            self.wb.write_data(row=self.row, column=9, msg=result)
