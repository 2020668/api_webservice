# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/14

E-mail:keen2020@outlook.com

=================================


"""

import pymysql


# step1:连接数据库
con = pymysql.connect(
    host="test.lemonban.com",
    port=3306,
    user="test",
    password="test",
    database="future",
    charset="utf8")

# step2:创建游标,并执行sql语句
cur = con.cursor()
sql = "SELECT LeaveAmount FROM member WHERE MobilePhone = 15071369970;"
# 返回查询到的数据的条数
res = cur.execute(sql)

# 获取1条数据
data = cur.fetchone()
print(data)
print(type(data))
print(data[0])
# 获取全部数据
# data = cur.fetchall()

# 获取指定数量的数据,3条
# data = cur.fetchmany(3)

# python连接mysql，默认开启了事务
# 进行增删改操作后，需提交事务 con.commit()
# demo
# cur.execute(sql)
# con.commit()
a = 100

