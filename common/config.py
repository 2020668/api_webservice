# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/4

E-mail:keen2020@outlook.com

=================================


"""

import configparser
import os
from common.constant import CONF_DIR


class ReadConfig(configparser.ConfigParser):

    def __init__(self):
        super().__init__()      # 调用父类的__init__方法
        # 读取后，就可以使用了conf.get()获取数据了
        self.read(os.path.join(CONF_DIR, 'env.ini'), encoding='utf8')
        version = self.get("env", "version")
        if version == "test":
            self.read(os.path.join(CONF_DIR, 'config_test.ini'), encoding='utf8')
        elif version == "produce":
            self.read(os.path.join(CONF_DIR, 'config_produce.ini'), encoding='utf8')

    def write_data(self, option, select, value):
        """
        :param option:
        :param select:
        :param data: 写入的数据，str
        :return:
        """
        self.set(option, select, value)
        with open(os.path.join(CONF_DIR, 'config_test.ini'), 'w') as f:     # 在config_test.ini中写入数据
            self.write(f)


conf = ReadConfig()

if __name__ == '__main__':
    r = ReadConfig()
    b = r.get('mysql', 'password')
    print(b)
    r.write_data('mysql', 'password', 'python999')
    b = r.get('mysql', 'password')
    print(b)
