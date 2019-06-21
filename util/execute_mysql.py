# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/15

E-mail:keen2020@outlook.com

=================================


"""

import pymysql
from common.config import conf


class ExecuteMysql(object):

    def __init__(self):

        # 连接数据库
        self.con = pymysql.connect(
            host=conf.get("mysql", "host"),
            port=conf.getint("mysql", "port"),
            user=conf.get("mysql", 'user'),
            password=conf.get("mysql", "password"),
            database=conf.get("mysql", "database"),
            charset="utf8")
        # 创建游标
        self.cur = self.con.cursor()

    def find_one(self, sql):

        # 执行sql语句
        self.cur.execute(sql)
        # 返回查询结果
        return self.cur.fetchone()

    def find_many(self, sql, number):

        # 执行sql语句
        self.cur.execute(sql)
        # 返回查询结果
        return self.cur.fetchmany(number)

    def find_all(self, sql):

        # 执行sql语句
        self.cur.execute(sql)
        return self.cur.fetchall()





