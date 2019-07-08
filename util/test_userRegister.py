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
class UserRegisterTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "userRegister")
    # wb = ReadExcel(os.path.join(DATA_DIR, file_name), "re")
    cases = wb.read_column_data(read_column)

    @classmethod
    def setUpClass(cls):

        my_log.info("准备开始执行注册接口的测试......")
        cls.request = HTTPRequest2()
        cls.db = ExecuteMysql()

    @data(*cases)   # 拆包，拆成几个参数
    def test_user_register(self, case):

        if "#phone#" in case.request_data:
            sql = "SELECT Fverify_code FROM sms_db_{}.t_mvcode_info_{} WHERE Fmobile_no={}".\
                format(case.mobile[9:11], case.mobile[8], case.mobile)
            mcode = self.db.find_one(sql)[0]
            print("查询语句为：{}".format(sql))
            case.request_data = case.request_data.replace('#mcode#', mcode)
            case.request_data = case.request_data.replace('#phone#', case.mobile)

        if "baozi" in case.request_data:
            user_name = v_code()
            case.request_data = case.request_data.replace("baozi", user_name)

        else:
            case.request_data = data_replace(case.request_data)

        # 拼接url地址
        url = conf.get("env", "url") + case.url
        self.row = case.case_id + 1
        web_service = client.Client(url=url)
        data = eval(case.request_data)
        res = web_service.service.userRegister(data)
        result = dict(res)
        # 成功服务器响应数据{'retCode': 0, 'retInfo': ok}，需将ok --> 'ok'
        if 'retCode' in str(result):
            result = {'retCode': result['retCode'], 'retInfo': str(result['retInfo'])}
        # 由于测试失败返回的数据特殊{'faultcode': soap:Server, 'faultstring': 手机号码错误}，只能转换为str再来断言
        else:
            print(str(eval(case.expected_data)['faultcode']))
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

        my_log.info("注册接口测试执行完毕......")
        cls.request.close()
        cls.db.close()
