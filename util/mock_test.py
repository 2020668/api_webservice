# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/7/3

E-mail:keen2020@outlook.com

=================================


"""

import requests
from unittest import mock


url = "http://127.0.0.1:8000/login"

data = {"user": "python", "pwd": "123456"}

request = mock.Mock(return_value={"code": 1, "msg": "登录成功"})
response = request(url=url, data=data)
print(response)

