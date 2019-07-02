# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/29

E-mail:keen2020@outlook.com

=================================


"""

import smtplib
from email.mime.text import MIMEText        # 构造邮件文本内容
from email.header import Header      # 构造邮件标题
from email.mime.application import MIMEApplication      # 发送带附件的邮件
from email.mime.multipart import MIMEMultipart      # 发送带附件的邮件
import win32com.client as win32
import datetime,os


class SendEmail(object):

    def send_163_mail(self):

        # 创建一个SMTP对象
        s = smtplib.SMTP()

        # 连接到SMTP服务器，QQ邮箱是服务器地址和端口465.网易的服务器是smtp.163.com端口25
        s.connect(host='smtp.163.com', port=25)

        # 登录SMTP服务器
        msg_from = 'tomcat666888@163.com'
        passwd = 'python1'
        msg_to = ["3023087535@qq.com", "415250069@qq.com", "87313199@qq.com"]
        s.login(user=msg_from, password=passwd)

        # 构建邮件内容
        content = "本次测试通过率99%"

        # 创建一个邮件，文本类型
        msg = MIMEText(content, _charset='utf8')
        # 添加邮件主题
        msg['Subject'] = Header('18期测试报告', 'utf-8')
        msg['From'] = msg_from
        msg['To'] = ','.join(msg_to)

        # 发送邮件
        try:
            s.sendmail(from_addr=msg_from, to_addrs=msg["To"].split(','), msg=msg.as_string())
            print("发送成功")
        except:
            print("发送失败")

    def send_qq_email(self):

        msg_from = '3023087535@qq.com'           # 发送方邮箱
        passwd = 'egxkxbfwyvdxdeje'     # 填入发送方邮箱的授权码
        receivers = ['415250069@qq.com', '87313199@qq.com']         # 收件人邮箱

        subject = '今日份的睡前小故事'             # 主题
        content = "本次测试通过率99%"              # 正文
        msg = MIMEText(content)          # 创建一个邮件，文本类型
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = ','.join(receivers)
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg['To'].split(','), msg.as_string())
            print("邮件发送成功")
        except:
            print("发送失败")
        finally:
            s.quit()

    def send_qq1_mail(self):

        # 创建一个SMTP对象并连接smtp服务
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)

        # 登录SMTP服务器
        msg_from = '3023087535@qq.com'
        passwd = 'egxkxbfwyvdxdeje'
        msg_to = ['415250069@qq.com', '87313199@qq.com']

        s.login(user=msg_from, password=passwd)

        # 构建邮件内容
        content = "本次测试通过率99%"

        # 创建一个邮件，文本类型
        msg = MIMEText(content, _charset='utf8')
        # 添加邮件主题
        msg['Subject'] = Header('180期', 'utf-8')
        msg['From'] = msg_from      # 可以修改成任意名称
        msg['To'] = ','.join(msg_to)

        # 发送邮件
        try:
            s.sendmail(from_addr=msg_from, to_addrs=msg["To"].split(','), msg=msg.as_string())
            print("发送成功")
        except:
            print("发送失败")
        finally:
            s.quit()

    def send_qq_file_mail(title, message, file_path):

        # 创建一个SMTP对象并连接smtp服务
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)

        # 登录SMTP服务器
        msg_from = '3023087535@qq.com'
        passwd = 'egxkxbfwyvdxdeje'
        msg_to = ['415250069@qq.com', '87313199@qq.com', 'keen2020@outlook.com']

        s.login(user=msg_from, password=passwd)

        # 构建邮件内容
        # message = "这是W1935的自动化测试报告，请注意查收！"
        # 创建一个邮件，文本类型
        content = MIMEText(message, _charset='utf8')

        # 构造附件
        part = MIMEApplication(open(file_path, 'rb').read(), _subtype=False)
        # part = MIMEApplication(open('20190629135418_report.html', 'rb').read(), _subtype=False)
        part.add_header('content-disposition', 'attachment', filename='report18.html')      # 自定义文件名称

        # 封装邮件添加邮件主题
        msg = MIMEMultipart()
        # 添加文本内容和附件
        msg.attach(content)
        msg.attach(part)

        msg['Subject'] = Header(title, 'utf-8')
        msg['From'] = msg_from      # 可以修改成任意名称
        msg['To'] = ','.join(msg_to)

        # 发送邮件
        try:
            s.sendmail(from_addr=msg_from, to_addrs=msg["To"].split(','), msg=msg.as_string())
            print("send qq_email successfully")
        except:
            print("send qq_mail failed")
        finally:
            s.quit()

    def send_outlook_file_mail(mail_title, mail_message, file_path):

        addressee = '3023087535@qq.com' + ';' + 'zuowei2019@outlook.com'  # 收件人邮箱列表
        cc = 'tomcat666888@163.com' + ';' + '87313199@qq.com'  # 抄送人邮件列表
        mail_path = file_path  # 获取测试报告路径
        olook = win32.Dispatch("outlook.Application")  # 固定写法
        mail = olook.CreateItem(0)  # 固定写法
        mail.To = addressee  # 收件人
        mail.CC = cc  # 抄送人
        # mail.Recipients.Add(addressee)
        mail.Subject = mail_title  # 邮件主题
        # mail.Attachments.Add(mail_path, 1, 1, "myFile")
        mail.Attachments.Add(mail_path)
        read = open(mail_path, encoding='utf-8')  # 打开需
        # 要发送的测试报告附件文件
        # content = read.read()  # 读取测试报告文件中的内容
        read.close()
        mail.Body = mail_message  # 将从报告中读取的内容，作为邮件正文中的内容
        try:
            mail.Send()  # 发送
            print("send outlook_email successfully")
        except:
            print("send outlook_email failed")