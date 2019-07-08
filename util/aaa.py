
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
# data = {"client_ip": "1", "tmpl_id": '1', "mobile": 14987699100}
#
# # res = web_service.service.sendMCode(data)
# # 默认result类型，转换成dict
# res = web_service.service.sendMCode(data)
# print(dict(res))
# # print(res["faultcode"])

# from suds import client
from common import client

# url = 'http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
url = 'http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
# 获取该地址下的webservice对象
web_service = client.Client(url=url)
# print(web_service)

# 构造请求参数
data = {"verify_code":"607183", "user_id":"baozi","channel_id":"1","pwd":"123456", 'mobile':'#13116097510#',"ip":"1.1.1.1"}

# res = web_service.service.sendMCode(data)
# 默认result类型，转换成dict
res = web_service.service.userRegister(data)
print(dict(res))
# print(res["faultcode"])


