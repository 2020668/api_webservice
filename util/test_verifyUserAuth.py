# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/7/3

E-mail:keen2020@outlook.com

=================================


"""

# # from suds import client
# from common import client
#
# url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
#
# # 获取该地址下的webservice对象
# web_service = client.Client(url=url)
# # print(web_service)
#
# # 构造请求参数
# data = {"client_ip": "1", "tmpl_id": '1', "mobile": 1558769910}
#
# # res = web_service.service.sendMCode(data)
# # 默认result类型，转换成dict
# res = web_service.service.sendMCode(data)
# print(dict(res))
# # print(res["faultcode"])


import unittest
from library.ddt import ddt, data
from common.read_excel import ReadExcel
from common.logger import my_log   # 可直接导入对象
from common.config import conf
import os
from common.constant import DATA_DIR
from common.http_request import HTTPRequest2
from common.execute_mysql import ExecuteMysql
from common.tools import data_replace, v_code
from common import client


# 从配置文件获取数据
file_name = conf.get('excel', 'file_name')
read_column = conf.get('excel', 'read_column')
read_column = eval(read_column)     # 将str转换成list


@ddt
class VerifyUserAuthTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "verifyUserAuth")
    # wb = ReadExcel(os.path.join(DATA_DIR, file_name), "re")
    cases = wb.read_column_data(read_column)

    @classmethod
    def setUpClass(cls):

        my_log.info("准备开始执行实名认证接口的测试......")
        cls.request = HTTPRequest2()
        cls.db = ExecuteMysql()

    @data(*cases)   # 拆包，拆成几个参数
    def test_verify_user_auth(self, case):

        # 拼接url地址
        url = conf.get("env", "url") + case.url
        self.row = case.case_id + 1
        web_service = client.Client(url=url)
        data = eval(case.request_data)
        res = web_service.service.verifyUserAuth(data)
        result = dict(res)
        # 成功服务器响应数据{'retCode': 0, 'retInfo': ok}，需将ok --> 'ok'
        if 'retCode' in str(result):
            result = {'retCode': result['retCode'], 'retInfo': str(result['retInfo'])}
        # 由于测试失败返回的数据特殊{'faultcode': soap:Server, 'faultstring': 手机号码错误}，只能转换为str再来断言
        else:
            result = str(result)

        # 该打印的内容会显示在报告中
        print("请求数据--> {}".format(case.request_data))
        print("期望结果---> {}".format(case.expected_data))
        print("服务器响应数据--> {}".format(result))
        print("服务器响应数据类型：{}".format(type(result)))

        try:
            # if 'retCode' in case.expected_data:
            #     self.assertEqual(eval(case.expected_data), result)
            # else:
            #     self.assertEqual(case.expected_data, str(result))
            self.assertEqual(eval(case.expected_data), result)

        except AssertionError as e:
            result = 'FAIL'
            my_log.exception(e)     # 将异常信息记录到日志
            raise e
        else:
            result = 'PASS'
            my_log.debug("预期结果：%s, 实际结果：%s, 测试通过" % (case.expected_data, str(result)))

        finally:
            self.wb.write_data(row=self.row, column=8, msg=result)

    @classmethod
    def tearDownClass(cls):

        my_log.info("实名认证接口测试执行完毕......")
        cls.request.close()
        cls.db.close()
