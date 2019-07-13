# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/7/9

E-mail:keen2020@outlook.com

=================================


"""

import suds
from suds import client


class WebRequests(object):

    def web_request2(self, url, interface, data):
        print('请求数据: {}'.format(data))

        self.webs = client.Client(url=url)      # 传入url，创建webservice对象，打印对象可查看对象内部的方法

        try:
             response = eval('self.webs.service.{}({})'.format(interface, data))    # 拼接参数，并将str转换成python语句

        except suds.WebFault as e:
            # 服务器返回的数据在e.fault内,可转换成dict
            return {'code': dict(e.fault)['faultcode'], 'msg': dict(e.fault)['faultstring']}
        else:
            return {'code': dict(response)['retCode'], 'msg': dict(response)['retInfo']}

    def web_request(self, url, interface, data):

        self.webs = client.Client(url=url)      # 传入url，创建webservice对象，打印对象可查看对象内部的方法

        try:
             response = eval('self.webs.service.{}({})'.format(interface, data))    # 拼接参数，并将str转换成python语句

        except suds.WebFault as e:
            # 服务器返回的数据在e.fault内,可转换成dict
            return dict(e.fault)
        else:
            return dict(response)


if __name__ == '__main__':
    url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
    data = {'client_ip': '1.1.1.1', 'tmpl_id': '1', 'mobile': '13368789990'}
    web = WebRequests()
    result = web.web_request(url=url, interface='sendMCode', data=data)
    print(result)
