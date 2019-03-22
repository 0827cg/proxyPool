#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-12-20 18:56
import time
import urllib.request
from bs4.dammit import UnicodeDammit


class TestProxy:

    header_obj = dict()
    header_obj['User-Agent'] = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                'like Gecko) Chrome/70.0.3538.110 Safari/537.36')

    def get_proxy_response(self, url):

        """
        返回一个httpResponse类型的数据, 请求出错返回None
        :param url: 需要请求的url
        :return: 返回一个httpResponse类型的数据, 请求出错返回None
        """

        http_response_data = None

        print('正在请求页面[' + url + ']')

        # print('正在连接代理服务器[' + str(proxyMsgObj) + ']')

        # proxyHandlerObj = urllib.request.ProxyHandler(proxies={'https': '218.59.228.18:61976'})
        # print(type(proxyHandlerObj))
        # print(proxyHandlerObj)
        # print(str(proxyHandlerObj))

        # openerDirectorObj = urllib.request.build_opener(proxyHandlerObj)
        # print(type(openerDirectorObj))
        # print(openerDirectorObj)
        # print(str(openerDirectorObj))

        index_request_time = time.time()
        try:
            req_obj = urllib.request.Request(url, headers=self.header_obj)
            req_obj.set_proxy('61.135.155.82:443', 'http')
            print(urllib.request.getproxies())
            # httpResponseData = openerDirectorObj.open(reqObj)
            http_response_data = urllib.request.urlopen(req_obj)

        except Exception as error:

            print('请求出错[error=' + str(error) + ']--耗时: ' +
                  str(round(time.time() - index_request_time, 4)) + 's')

        else:

            int_code = http_response_data.getcode()

            print(str(http_response_data.info()))
            print('response url:[' + http_response_data.geturl() + ']')

            if int_code == 200:
                print('请求成功---耗时: ' + str(round(time.time() - index_request_time, 4)) + 's')
            else:
                http_response_data = None
                print('请求出错[code=' + str(int_code) + ']--耗时: ' +
                      str(round(time.time() - index_request_time, 4)) + 's')

        return http_response_data

    def get_proxy_str_msg_new(self, url):

        """
        describe: 根据url来获取页面的源代码内容, 这里通过使用UnicodeDammit这个模块来获取页面编码及内容
        :param url: 需要获取的页面的url
        :return: 返回页面数据, 为str类型, 如果请求出错, 则页面数据返回None
        """
        http_response_data = self.get_proxy_response(url)

        if http_response_data is not None:

            bytes_data = http_response_data.read()

            ud_obj = UnicodeDammit(bytes_data)
            str_html = ud_obj.unicode_markup

            http_response_data.close()
        else:
            str_html = None
        # print(httpResponseData.closed)
        return str_html


str_url = 'http://2018.ip138.com/ic.asp'
str_page_content = TestProxy().get_proxy_str_msg_new(str_url)
print(str_page_content)