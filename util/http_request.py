# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/13

E-mail:keen2020@outlook.com

=================================


"""

import requests
from requests.sessions import Session
from common.logger import my_log

"""
封装requests类，根据用例中的请求方法，来决定发起什么类型的请求。输出logging日志
"""


class HTTPRequest(object):
    """不记录cookies信息给下一次请求使用"""
    def request(self, method, url,
                params=None, data=None,
                headers=None, cookies=None, json=None):

        method = method.lower()
        if method == "post":
            # 判断是否使用json来传参（适用于接口项目有使用json传参）
            if json:
                my_log.info("正在发送请求，请求地址：{}， 请求参数：{}".format(url, json))
                return requests.post(url=url, json=json, headers=headers, cookies=cookies)
            else:
                my_log.info("正在发送请求，请求地址：{}， 请求参数：{}".format(url, data))
                return requests.post(url=url, data=data, headers=headers, cookies=cookies)
        elif method == "get":
            my_log.info("正在发送请求，请求地址：{}， 请求参数：{}".format(url, params))
            return requests.get(url=url, params=params, headers=headers, cookies=cookies)


class HTTPRequest2(object):
    """记录cookies信息给下一次请求使用"""

    def __init__(self):
        # 创建session对象
        self.session = Session()

    def request(self, method, url,
                params=None, data=None,
                headers=None, cookies=None, json=None):

        method = method.lower()
        if method == "post":
            # 判断是否使用json来传参（适用于接口项目有使用json传参）
            if json:
                my_log.info("正在发送请求，请求地址：{}， 请求参数：{}".format(url, json))
                return self.session.post(url=url, json=json, headers=headers, cookies=cookies)
            else:
                my_log.info("正在发送请求，请求地址：{}， 请求参数：{}".format(url, data))
                return self.session.post(url=url, data=data, headers=headers, cookies=cookies)
        elif method == "get":
            my_log.info("正在发送请求，请求地址：{}， 请求参数：{}".format(url, params))
            return self.session.get(url=url, params=params, headers=headers, cookies=cookies)


if __name__ == '__main__':
    r = HTTPRequest2()
    mobilephone = "15071337986"

    # 登录
    login_url = "http://test.lemonban.com/futureloan/mvc/api/member/login"
    data = {"mobilephone": mobilephone, "pwd": "123456"}
    response = r.request(method="post", url=login_url, data=data)
    html_login = response.content.decode()
    print(html_login)

    # 充值
    recharge_url = "http://test.lemonban.com/futureloan/mvc/api/member/recharge"
    data = {"mobilephone": mobilephone, "amount": 500000}
    response = r.request(method="post", url=recharge_url, data=data)
    html_recharge = response.content.decode()
    print(html_recharge)
