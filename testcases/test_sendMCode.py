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
from common.read_excel import ReadExcel
from common.logger import my_log   # 可直接导入对象
from common.config import conf
import os
from common.constant import DATA_DIR
from common.http_request import HTTPRequest2
from common.execute_mysql import ExecuteMysql
from common.tools import data_replace, rand_ip
from common.web_request import WebRequests


# 从配置文件获取数据
file_name = conf.get('excel', 'file_name')
read_column = conf.get('excel', 'read_column')
read_column = eval(read_column)     # 将str转换成list


@ddt
class SendMCodeTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "sendMCode")
    cases = wb.read_column_data(read_column)

    @classmethod
    def setUpClass(cls):

        my_log.info("======准备开始执行发送短信验证码接口的测试======")
        cls.request = HTTPRequest2()
        cls.db = ExecuteMysql()

    @classmethod
    def tearDownClass(cls):
        my_log.info("======发送短信验证码接口测试执行完毕======")
        cls.request.close()
        cls.db.close()

    @data(*cases)   # 拆包，拆成几个参数
    def test_send_m_code(self, case):

        # 替换成随机手机号码
        case.request_data = data_replace(case.request_data)

        # 替换成随机ip
        case.request_data = case.request_data.replace('$ip', rand_ip())

        # 拼接url地址
        url = conf.get("env", "url") + case.url
        self.row = case.case_id + 1

        # 调用封装好的webservice请求方法
        webs = WebRequests()
        response = webs.web_request(url=url, interface='sendMCode', data=case.request_data)

        # 用例失败则返回的键值不是str,会报错,需将值转换为str
        if 'faultcode' in response:
            response = {'faultcode': str(response.get('faultcode')), 'faultstring': str(response.get('faultstring'))}

        # 该打印的内容会显示在报告中,以及日志
        print("请求参数--> {}".format(case.request_data))
        my_log.info('请求参数--> {}'.format(case.request_data))

        print("期望结果---> {}".format(case.expected_data))
        my_log.info("期望结果---> {}".format(case.expected_data))

        print("服务器响应数据--> {}".format(response))
        my_log.info("服务器响应数据--> {}".format(response))

        try:
            if 'retCode' in case.expected_data:
                self.assertEqual(eval(case.expected_data), response)
            else:
                self.assertEqual(case.expected_data, str(response))

        except AssertionError as e:
            result = 'FAIL'
            self.wb.write_data(row=self.row, column=9, msg=result)
            my_log.exception(e)     # 将异常信息记录到日志
            raise e
        else:
            result = 'PASS'
            my_log.info("断言结果--> {}, 测试通过".format(result))
        finally:
            self.wb.write_data(row=self.row, column=8, msg=str(response))   # 只能写入str类型数据
            self.wb.write_data(row=self.row, column=9, msg=result)

        # if '正常' in case.title:
        #     mobile = eval(case.request_data)['mobile']
            # self.wb.close()
            # wb1 = ReadExcel(os.path.join(DATA_DIR, file_name), "userRegister")
            # wb1.write_data(row=self.row, column=10, msg=mobile)
