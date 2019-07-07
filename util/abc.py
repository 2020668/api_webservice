# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/7/5

E-mail:keen2020@outlook.com

=================================


"""

from common import client

url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'

# 获取该地址下的webservice对象
web_service = client.Client(url=url)
# print(web_service)

# 构造请求参数
data = {"client_ip": "2", "tmpl_id": '2', "mobile": '13398392930'}

# res = web_service.service.sendMCode(data)
# 默认result类型，转换成dict
res = web_service.service.sendMCode(data)
print(dict(res))
# print(res["faultcode"])

