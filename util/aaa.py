
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


# from common import client
#
# # url = 'http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
# url = 'http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
# # 获取该地址下的webservice对象
# web_service = client.Client(url=url)
#
#
# # 构造请求参数
# data = {"verify_code":"012393", "user_id":"baoi","channel_id":"1","pwd":"123456", 'mobile':'13089905136',"ip":"1.1.1.1"}
#
#
# # 默认result类型，转换成dict
# res = web_service.service.userRegister(data)
# print(dict(res))


# python随机生成包含字母数字的六位验证码
# import random
#
#
# def v_code():
#     ret = ""
#     for i in range(6):
#         num = random.randint(0, 9)
#         # num = chr(random.randint(48,57))#ASCII表示数字
#         letter = chr(random.randint(97, 122))#取小写字母
#         Letter = chr(random.randint(65, 90))#取大写字母
#         s = str(random.choice([num,letter,Letter]))
#         ret += s
#     return ret

# from common import client
#
# # url = 'http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
# url = 'http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
# # 获取该地址下的webservice对象
# web_service = client.Client(url=url)
#
#
# # 构造请求参数
# data = {"uid":"128736679730", "true_name":"陈晶晶","cre_id":"42112619880909724"}
#
#
# # 默认result类型，转换成dict
# res = web_service.service.verifyUserAuth(data)
# print(dict(res))

# import random
#
#
# def rand_ip():
#     ip = '{}.{}.{}.{}'.format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
#     return ip
#
#
# ip = rand_ip()
# print(ip)

# 获取指定字符串后的字符，如：phone后面的130

def m_code(ip, mobile):
    data = {'client_ip': ip, 'tmpl_id': '1', 'mobile': mobile}
    url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'







