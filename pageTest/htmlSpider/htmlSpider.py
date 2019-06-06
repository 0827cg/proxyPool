#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe: 解析页面用的spider
# author: cg
# time: 2018-10-24 16-33

import urllib.request
import time
import socket
from bs4 import BeautifulSoup
from bs4.dammit import UnicodeDammit
from .header import header_obj
from proxyPool.bin.proxy_pool import ProxyPool


class HtmlSpider(ProxyPool):

    # 设置超时时间
    time_out = 10
    socket.setdefaulttimeout(time_out)

    def getresponse(self, url):
        """
        describe: 请求url, 获取响应内容
        :param url: 需要请求的url
        :return: 返回一个httpResponse类型的数据, 请求出错返回None
        """
        try:
            req_obj = urllib.request.Request(url, headers=header_obj)
            http_response_data = urllib.request.urlopen(req_obj)
            return http_response_data
        except BaseException as error:
            self.log_obj.error('请求出错, url: ' + url + ' error: ' + str(error))
            return None

    def getresponse_proxy(self, url, proxy_msg):
        """
        describe: 请求url, 获取响应内容, 使用代理方式
        :param url: 需要请求的url
        :param proxy_msg: 代理服务器信息
        :return: 返回一个httpResponse类型的数据, 请求出错返回None
        """
        proxy_handler_obj = urllib.request.ProxyHandler(proxy_msg)
        opener_director_obj = urllib.request.build_opener(proxy_handler_obj)
        try:
            req_obj = urllib.request.Request(url, headers=header_obj)
            http_response_data = opener_director_obj.open(req_obj)
            return http_response_data
        except Exception as error:
            self.log_obj.error('请求出错, url: ', url, ' proxy_msg: ', proxy_msg,  ' error: ', str(error))
            return None

    def getresponse_proxy_msg(self, url, proxy_host, proxy_type):

        """
        describe: 请求url, 获取响应内容, 使用代理方式
        :param url: 需要请求的url
        :param proxy_host: 代理服务器ip和端口port, 格式: ip:port
        :param proxy_type: 代理服务器协议类型, https/http
        :return: 返回一个httpResponse类型的数据, 请求出错返回None
        """
        try:
            req_obj = urllib.request.Request(url, headers=header_obj)
            req_obj.set_proxy(proxy_host, proxy_type)
            http_response_data = urllib.request.urlopen(req_obj)
            return http_response_data
        except Exception as error:
            self.log_obj.error('请求出错, url: ', url + ' proxy_host: ', proxy_host,  ' proxy_type: ',
                               proxy_type, ' error: ' + str(error))
            return None

    def get_html_msg(self, url):
        """
        describe: 根据url获取页面数据,
        :param url: 需要获取的页面的url
        :return: 返回页面数据, 为bytes类型, 如果请求结果为None, 则返回页面数据为None
        """
        http_response_data = self.getresponse(url)
        if http_response_data is not None:
            # 读取响应体
            bytes_data = http_response_data.read()
            http_response_data.close()
        else:
            bytes_data = None
        return bytes_data

    def get_html_msg_proxy(self, url, proxy_msg_obj):
        """
        describe: 根据url获取页面数据, 使用代理方式
        :param url: 需要获取的页面的url
        :param proxy_msg_obj: 代理服务器信息
        :return: 返回页面数据, 为bytes类型, 如果请求结果为None, 则返回页面数据为None
        """
        http_response_data = self.getresponse_proxy(url, proxy_msg_obj)
        if http_response_data is not None:
            # 读取响应体
            bytes_data = http_response_data.read()
            http_response_data.close()
        else:
            bytes_data = None
        return bytes_data

    def get_html_msg_str(self, url):
        """
        根据url来获取页面的源代码内容, 已按页面编码来解码, 如为获取到页面编码, 则默认使用utf-8编码
        :param url: 需要获取的页面的url
        :return:  返回页面数据, 为str类型, 如果请求出错, 则页面数据返回None
        """
        http_response_data = self.getresponse(url)
        if http_response_data is not None:
            code = http_response_data.headers.get_content_charset()
            bytes_data = http_response_data.read()
            if code is None:
                code = self.get_page_encode(bytes_data)
                if code is None:
                    code = 'utf-8'
            str_html = bytes_data.decode(code, 'ignore')
            http_response_data.close()
        else:
            str_html = None
        return str_html

    def get_html_str_msg_new(self, url):

        """
        describe: 根据url来获取页面的源代码内容, 这里通过使用UnicodeDammit这个模块来获取页面编码及内容
        :param url: 需要获取的页面的url
        :return: 返回页面数据, 为str类型, 如果请求出错, 则页面数据返回None
        """
        http_response_data = self.get_html_http_response(url)
        if http_response_data is not None:
            bytes_data = http_response_data.read()
            ud_obj = UnicodeDammit(bytes_data)
            str_html = ud_obj.unicode_markup
            http_response_data.close()
        else:
            str_html = None
        # print(http_response_data.closed)
        return str_html

    def get_proxy_html_str_msg(self, url, proxy_host, proxy_type):
        """
        describe: 根据url来获取页面的源代码内容, 已按页面编码来解码, 如为获取到页面编码, 则默认使用utf-8编码. 使用代理方式
        :param url:
        :param proxy_host:
        :param proxy_type:
        :return: 返回页面数据, 为str类型, 如果请求出错, 则页面数据返回None
        """
        http_response_data = self.get_proxy_html_response_use_set(url, proxy_host, proxy_type)
        if http_response_data is not None:
            code = http_response_data.headers.get_content_charset()
            bytes_data = http_response_data.read()
            if code is not None:
                pass
            else:
                code = self.get_page_encode(bytes_data)
                if code is None:
                    print('未获取到页面编码, 执行默认设置为utf-8')
                    code = 'utf-8'
            str_html = bytes_data.decode(code, 'ignore')
            http_response_data.close()
        else:
            str_html = None
        return str_html

    def get_proxy_html_str_msg_new(self, url, proxy_host, proxy_type):
        """
        describe: 根据url来获取页面的源代码内容, 这里通过使用UnicodeDammit这个模块来获取页面编码及内容
        :param url: 需要获取的页面的url
        :param proxy_host:
        :param proxy_type:
        :return: 返回页面数据, 为str类型, 如果请求出错, 则页面数据返回None
        """
        http_response_data = self.get_proxy_html_response_use_set(url, proxy_host, proxy_type)
        if http_response_data is not None:
            bytes_data = http_response_data.read()
            ud_obj = UnicodeDammit(bytes_data)
            str_html = ud_obj.unicode_markup
            http_response_data.close()
        else:
            str_html = None
        return str_html

    @staticmethod
    def get_buildup_proxy_msg_obj(proxy_method, proxy_ip, port):
        """
        describe: 将ip地址, 端口和协议组装正代理需要的格式对象, 并返回

        如: 'http', '58.53.128.83', 3128  这三个参数, 得到的数据如: {'http': '58.53.128.83:3128'}
        :param proxy_method: 协议, http/https
        :param proxy_ip: ip地址
        :param port: 端口
        :return: dict类型
        """
        ip = proxy_ip + ":" + str(port)
        dict_msg = dict()
        dict_msg[proxy_method] = ip
        return dict_msg

    @staticmethod
    def get_html_encode(data):
        """
        describe: 获取网页的编码
        :param data: 网页内容, 可string, 可bytes
        :return: 返回编码, str类型
        """
        str_encode = None
        if data is not None:
            beautiful_obj = BeautifulSoup(data, "lxml")
            tag_label = beautiful_obj.find('meta', charset=True)
            if tag_label is not None:
                str_encode = tag_label['charset']
        else:
            print('参数[data=None]')
        print('获取到的页面编码为: ' + str(str_encode))
        return str_encode

    @staticmethod
    def get_page_encode(data):
        """
        describe: 获取网页的编码, 这个方法比getHtmlEncode()方法成功率更高
        :param data: 网页内容
        :return: 返回编码, str类型
        """
        if data is not None:
            ud_obj = UnicodeDammit(data)
            str_encode = ud_obj.original_encoding
            return str_encode
        else:
            return None

    def get_div_label_by_class_value(self, url, value):
        """
        describe: 获取div标签, 根据div标签中的class属性值来在规定页面获取
        :param url: 页面的url
        :param value: div标签中的class属性的值
        :return: 返回存放该标签的ResultSet类型数据, 如果请求出错, 则页面数据返回None
        """
        bytes_data = self.get_html_msg(url)
        if bytes_data is not None:
            beautiful_obj = BeautifulSoup(bytes_data, "html.parser")
            result_set_label = beautiful_obj.findAll('div', {'class': value})
        else:
            print('请求的页面[url=' + url + ']数据为None')
            result_set_label = None
        return result_set_label

    @staticmethod
    def get_div_label_by_class_value_on_data(data, value):
        """
        describe: 获取div标签, 在已有的页面数据基础上,根据div标签中的class属性值来在规定页面获取
        :param data: 页面的数据, 可为bytes类型,和str类型
        :param value: div标签中的class属性的值
        :return: 返回存放该标签的ResultSet类型数据
        """
        if data is not None:
            beautiful_obj = BeautifulSoup(data, 'html.parser')
            result_set_label = beautiful_obj.find_all('div', class_=value)
            print('爬取到[div]的标签如: ' + str(result_set_label))
        else:
            print('传入的[data=None], 结果为None')
            result_set_label = None
        return result_set_label

    def get_label_by_text(self, url, label_name, text):

        """
        describe: 根据标签的名字和标签的内容值来在规定的url页面中获取需要的标签
        :param url: 需要打开的页面路径
        :param label_name: 需要获取的标签名字
        :param text: 标签里面的内容
        :return: 返回一个存放标签的ResultSet类型数据
        """
        bytes_data = self.get_html_msg(url)
        if bytes_data is not None:
            beautiful_obj = BeautifulSoup(bytes_data, "html.parser")
            result_set_label = beautiful_obj.find_all(label_name, text=text)

            print('爬取[text=' + text + ']的[' + label_name + ']标签如: ' + str(result_set_label))
        else:
            print('请求的页面[strUtl=' + url + ']数据为None, 结果为空')
            result_set_label = None

        return result_set_label

    @staticmethod
    def get_label_by_text_on_data(data, label_name, text):
        """
        describe: 在已有的页面数据基础上, 根据标签的名字和标签的内容值来获取标签
        :param data: bytes类型的页面数据, 也可为str类型
        :param label_name: 需要获取的标签名
        :param text: 需要获取的标签的内容值
        :return: 返回一个存放标签的ResultSet类型数据
        """
        if data is not None:
            beautiful_obj = BeautifulSoup(data, "html.parser")
            result_set_label = beautiful_obj.find_all(label_name, text=text)
            print('爬取到[text=' + text + ']的[' + label_name + ']标签如: ' + str(result_set_label))

        else:
            print('传入的[data=None], 结果为None')
            result_set_label = None
        return result_set_label

    @staticmethod
    def get_label_by_key_value_on_data(data, label_name, key, value):

        """
        describe: 在已有的页面数据基础上, 根据标签的名字和标签的属性及属性值来获取标签, 只会获取一个, 所以要求参数值是页面中的唯一
        :param data: 页面数据, 可为bytes, str类型
        :param label_name: 需要获取的标签名
        :param key: 需要获取的标签的属性名
        :param value: 需要获取的标签的属性名的值
        :return: 返回一个bs4.element.Tag类型的数据
        """
        if data is not None:
            beautiful_obj = BeautifulSoup(data, "html.parser")
            tag_label = beautiful_obj.find(label_name, {key: value})
            print('爬取到[' + key + '=' + value + ']的[' + label_name + ']标签如: ' + str(tag_label))
        else:
            print('传入的[data=None], 结果为None')
            tag_label = None

        return tag_label

    # @staticmethod
    # def get_label_by_key_value_on_data(data, label_name, key, value):
    #
    #     """
    #     describe: 在已有的页面数据基础上, 根据标签的名字和标签的属性及属性值来获取标签, 只会获取一个, 所以要求参数值是页面中的唯一
    #     :param data: 页面数据, 可为bytes, str类型
    #     :param label_name: 需要获取的标签名
    #     :param key: 需要获取的标签的属性名
    #     :param value: 需要获取的标签的属性名的值
    #     :return: 返回一个bs4.element.Tag类型的数据
    #     """
    #     if data is not None:
    #         beautiful_obj = BeautifulSoup(data, "html.parser")
    #         result_set_label = beautiful_obj.find_previous_siblings(label_name, {key: value})
    #
    #         print('爬取到[' + key + '=' + value + ']的[' +
    #                                   label_name + ']标签如: ' + str(result_set_label))
    #
    #     else:
    #         print('传入的[data=None], 结果为None')
    #         result_set_label = None
    #     return result_set_label

    @staticmethod
    def get_label_by_more_key_value_on_data(data, label_name, **kwargs):

        """
        describe: 在已有的页面数据基础上, 根据标签的名字和多个标签的属性及属性值来获取标签(目前不支持class 和text, 暂时废弃)
        :param data: 页面数据, 可为bytes, str类型
        :param label_name: 需要获取的标签名
        :param kwargs: 键值对类型数据, 如, class='xxx', title='xxx'
        :return: 返回一个存放标签的resultSet类型数据
        """
        if data is not None:

            beautiful_obj = BeautifulSoup(data, "html.parser")
            result_set_label = beautiful_obj.find_all(label_name, kwargs)

            print('爬取到[kwargs=' + str(kwargs) + ']的[' + label_name + ']标签如: ' + str(result_set_label))
        else:
            print('传入的[data=None], 结果为None')
            result_set_label = None

        return result_set_label

    def get_label_key_value(self, url, label_name, text, key):

        """
        describe: 在规定的页面里, 根据标签名和标签的内容值, 来获取该标签所含有的属性的值
        :param url: 页面url
        :param label_name: 标签名
        :param text: 标签的内容值
        :param key: 需要获取的标签中的属性的名字
        :return: 返回标签中的该属性的值, 为str类型数据
        """

        print('正在爬取[ text=' + text + ' ]的标签key=' + key + '的值....')
        value = ''
        result_set_label = self.get_label_by_text(url, label_name, text)
        for tag_item in result_set_label:
            value = tag_item.get(key)

        print('爬取完成,[' + key + ']的值为' + value)
        return value

    def get_label_key_value_on_data(self, data, label_name, text, key):

        """
        escribe: 在已知的页面数据中, 根据标签名和标签的内容值, 来获取该标签所含有的属性的值
        :param data: 已知的页面数据, bytes类型或str类型
        :param label_name: 标签名
        :param text: 标签的内容值
        :param key: 需要获取的标签中的属性的名字
        :return: 返回标签中的该属性的值, 为str类型数据
        """

        if data is not None:
            print('正在从页面内容中解析爬取[text=' + text + ']的标签key=' + key + '的值....')

            index_time = time.time()

            value = ''
            result_set_label = self.get_label_by_text_on_data(data, label_name, text)
            for tag_item in result_set_label:
                value = tag_item.get(key)
            print('爬取完成,[' + key + ']的值为' + value + '---耗时: ' + str(round(time.time() - index_time, 4)) + 's')
        else:
            print('传入的[data=None], 结果为None')
            value = None
        return value
