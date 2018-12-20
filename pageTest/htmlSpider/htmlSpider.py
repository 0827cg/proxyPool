#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe: 解析页面用的spider
# author: cg
# time: 2018-10-24 16-33

import urllib.request
import time
import re
import socket
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit

from .header import headerObj


class HtmlSpider:

    # 设置超时时间
    intTimeout = 10
    socket.setdefaulttimeout(intTimeout)

    def getHtmlHttpReponse(self, strUrl):

        '''
        describe: 请求url, 获取响应内容
        :param strUrl: 需要请求的url
        :return: 返回一个httpResponse类型的数据, 请求出错返回None
        '''

        print('正在请求页面[' + strUrl + ']')
        intIndexTime = time.time()

        httpResponseData = None
        try:
            reqObj = urllib.request.Request(strUrl, headers=headerObj)
            httpResponseData = urllib.request.urlopen(reqObj)

        except Exception as error:
            print('请求出错[error=' + str(error) + ']--耗时: ' +
                                      str(round(time.time() - intIndexTime, 4)) + 's')
        else:

            intCode = httpResponseData.getcode()

            print(str(httpResponseData.info()))
            print('response url:[' + httpResponseData.geturl() + ']')

            if intCode == 200:
                print('请求成功---耗时: ' + str(round(time.time() - intIndexTime, 4)) + 's')
            else:
                httpResponseData = None
                print('请求出错[code=' + str(intCode) + ']--耗时: '+
                                          str(round(time.time() - intIndexTime, 4)) + 's')

        return httpResponseData


    def getProxyHtmlHttpReponse(self, strUrl, proxyMsgObj):

        '''
        describe: 请求url, 获取响应内容, 使用代理方式
        :param strUrl: 需要请求的url
        :param proxyMsgObj: 代理服务器信息
        :return: 返回一个httpResponse类型的数据, 请求出错返回None
        '''

        httpResponseData = None

        print('正在请求页面[' + strUrl + ']')

        print('正在连接代理服务器[' + str(proxyMsgObj) + ']')

        proxyHandlerObj = urllib.request.ProxyHandler(proxyMsgObj)
        # print(type(proxyHandlerObj))
        # print(proxyHandlerObj)
        # print(str(proxyHandlerObj))

        openerDirectorObj = urllib.request.build_opener(proxyHandlerObj)
        # print(type(openerDirectorObj))
        # print(openerDirectorObj)
        # print(str(openerDirectorObj))

        intIndexRequestTime = time.time()
        try:
            reqObj = urllib.request.Request(strUrl, headers=headerObj)
            httpResponseData = openerDirectorObj.open(reqObj)

        except Exception as error:

            print('请求出错[error=' + str(error) + ']--耗时: ' +
                  str(round(time.time() - intIndexRequestTime, 4)) + 's')

        else:

            intCode = httpResponseData.getcode()

            print(str(httpResponseData.info()))
            print('response url:[' + httpResponseData.geturl() + ']')

            if intCode == 200:
                print('请求成功---耗时: ' + str(round(time.time() - intIndexRequestTime, 4)) + 's')
            else:
                httpResponseData = None
                print('请求出错[code=' + str(intCode) + ']--耗时: ' +
                      str(round(time.time() - intIndexRequestTime, 4)) + 's')

        return httpResponseData


    def getProxyHtmlHttpReponseUseSet(self, strUrl, strProxyHost, strProxyType):

        '''
        describe: 请求url, 获取响应内容, 使用代理方式
        :param strUrl: 需要请求的url
        :param strProxyHost: 代理服务器ip和端口port, 格式: ip:port
        :param strProxyType: 代理服务器协议类型, https/http
        :return: 返回一个httpResponse类型的数据, 请求出错返回None
        '''

        httpResponseData = None

        print('正在请求页面[' + strUrl + ']')

        print('正在连接代理服务器[host=' + strProxyHost + ', type=' + strProxyType + ']')

        intIndexRequestTime = time.time()
        try:
            reqObj = urllib.request.Request(strUrl, headers=headerObj)
            reqObj.set_proxy(strProxyHost, strProxyType)
            httpResponseData = urllib.request.urlopen(reqObj)

        except Exception as error:

            print('请求出错[error=' + str(error) + ']--耗时: ' +
                  str(round(time.time() - intIndexRequestTime, 4)) + 's')

        else:

            intCode = httpResponseData.getcode()

            print(str(httpResponseData.info()))
            print('response url:[' + httpResponseData.geturl() + ']')

            if intCode == 200:
                print('请求成功---耗时: ' + str(round(time.time() - intIndexRequestTime, 4)) + 's')
            else:
                httpResponseData = None
                print('请求出错[code=' + str(intCode) + ']--耗时: ' +
                      str(round(time.time() - intIndexRequestTime, 4)) + 's')

        return httpResponseData


    def getHtmlMsg(self, strUrl):

        '''
        describe: 根据url获取页面数据,
        :param strUrl: 需要获取的页面的url
        :return: 返回页面数据, 为bytes类型, 如果请求结果为None, 则返回页面数据为None
        '''

        httpResponseData = self.getHtmlHttpReponse(strUrl)

        if httpResponseData is not None:

            # 读取响应体
            bytesData = httpResponseData.read()

            httpResponseData.close()
        else:
            print('请求页面结果数据为None')
            bytesData = None
        return bytesData


    def getProxyHtmlMsg(self, strUrl, proxyMsgObj):

        '''
        describe: 根据url获取页面数据, 使用代理方式
        :param strUrl: 需要获取的页面的url
        :param proxyMsgObj: 代理服务器信息
        :return: 返回页面数据, 为bytes类型, 如果请求结果为None, 则返回页面数据为None
        '''

        httpResponseData = self.getProxyHtmlHttpReponse(strUrl, proxyMsgObj)

        if httpResponseData is not None:

            # 读取响应体
            bytesData = httpResponseData.read()

            httpResponseData.close()
        else:
            print('请求页面结果数据为None')
            bytesData = None
        return bytesData


    def getHtmlStrMsg(self, strUrl):

        '''
        describe: 根据url来获取页面的源代码内容, 已按页面编码来解码, 如为获取到页面编码, 则默认使用utf-8编码
        :param strUrl: 需要获取的页面的url
        :return: 返回页面数据, 为str类型, 如果请求出错, 则页面数据返回None
        '''

        httpResponseData = self.getHtmlHttpReponse(strUrl)

        if httpResponseData is not None:
            strCoding = httpResponseData.headers.get_content_charset()
            bytesData = httpResponseData.read()

            if strCoding is not None:
                pass
            else:
                # strCoding = self.getHtmlEncode(bytesData)
                strCoding = self.getPageEncode(bytesData)

                if strCoding is None:
                    print('未获取到页面编码, 执行默认设置为utf-8')
                    strCoding = 'utf-8'
            strHtml = bytesData.decode(strCoding, 'ignore')

            httpResponseData.close()
        else:
            strHtml = None
        # print(httpResponseData.closed)
        return strHtml

    def getHtmlStrMsgNew(self, strUrl):

        '''
        describe: 根据url来获取页面的源代码内容, 这里通过使用UnicodeDammit这个模块来获取页面编码及内容
        :param strUrl: 需要获取的页面的url
        :return: 返回页面数据, 为str类型, 如果请求出错, 则页面数据返回None
        '''

        httpResponseData = self.getHtmlHttpReponse(strUrl)

        if httpResponseData is not None:

            bytesData = httpResponseData.read()

            udObj = UnicodeDammit(bytesData)
            strHtml = udObj.unicode_markup

            httpResponseData.close()
        else:
            strHtml = None
        # print(httpResponseData.closed)
        return strHtml

    def getProxyHtmlStrMsg(self, strUrl, strProxyHost, strProxyType):

        '''
        describe: 根据url来获取页面的源代码内容, 已按页面编码来解码, 如为获取到页面编码, 则默认使用utf-8编码. 使用代理方式
        :param strUrl: 需要获取的页面的url
        :param proxyMsgObj: 代理服务器信息
        :return: 返回页面数据, 为str类型, 如果请求出错, 则页面数据返回None
        '''

        httpResponseData = self.getProxyHtmlHttpReponseUseSet(strUrl, strProxyHost, strProxyType)

        if httpResponseData is not None:
            strCoding = httpResponseData.headers.get_content_charset()
            bytesData = httpResponseData.read()

            if strCoding is not None:
                pass
            else:
                strCoding = self.getPageEncode(bytesData)
                if strCoding is None:
                    print('未获取到页面编码, 执行默认设置为utf-8')
                    strCoding = 'utf-8'
            strHtml = bytesData.decode(strCoding, 'ignore')

            httpResponseData.close()
        else:
            strHtml = None
        return strHtml


    def getProxyHtmlStrMsgNew(self, strUrl, strProxyHost, strProxyType):

        '''
        describe: 根据url来获取页面的源代码内容, 这里通过使用UnicodeDammit这个模块来获取页面编码及内容
        :param strUrl: 需要获取的页面的url
        :param proxyMsgObj: 代理服务器信息
        :return: 返回页面数据, 为str类型, 如果请求出错, 则页面数据返回None
        '''

        httpResponseData = self.getProxyHtmlHttpReponseUseSet(strUrl, strProxyHost, strProxyType)

        if httpResponseData is not None:

            bytesData = httpResponseData.read()

            udObj = UnicodeDammit(bytesData)
            strHtml = udObj.unicode_markup

            httpResponseData.close()
        else:
            strHtml = None
        # print(httpResponseData.closed)
        return strHtml



    def getBuildUpProxyMsgObj(self, strProxyMethod, strProxyIP, intPort):

        '''
        describe: 将ip地址, 端口和协议组装正代理需要的格式对象, 并返回

        如: 'http', '58.53.128.83', 3128  这三个参数, 得到的数据如: {'http': '58.53.128.83:3128'}
        :param strProxyMethod: 协议, http/https
        :param strProxyIP: ip地址
        :param intPort: 端口
        :return: dict类型
        '''

        strFullIP = strProxyIP + ":" + str(intPort)
        dictMsg = {}
        dictMsg[strProxyMethod] = strFullIP

        return dictMsg


    def getHtmlEncode(self, data):

        '''
        describe: 获取网页的编码
        :param data: 网页内容, 可string, 可bytes
        :return: 返回编码, str类型
        '''
        strEncode = None

        if data is not None:

            beautifulObj = BeautifulSoup(data, "lxml")

            tagLabel = beautifulObj.find('meta', charset=True)

            if tagLabel is not None:
                strEncode = tagLabel['charset']
        else:
            print('参数[data=None]')

        print('获取到的页面编码为: ' + str(strEncode))
        return strEncode


    def getPageEncode(self, data):

        '''
        describe: 获取网页的编码, 这个方法比getHtmlEncode()方法成功率更高
        :param data: 网页内容
        :return: 返回编码, str类型
        '''

        strEncode = None

        if data is not None:

            print('unicodeDammit....')
            udObj = UnicodeDammit(data)

            strEncode = udObj.original_encoding

            print('unicodeDammit---over')
        else:
            print('参数[data=None]')

        print('获取到的页面编码为: ' + str(strEncode))
        return strEncode



    def getDivLabelByClassValue(self, strUrl, strValue):

        '''
        describe: 获取div标签, 根据div标签中的class属性值来在规定页面获取
        :param strUrl: 页面的url
        :param strValue: div标签中的class属性的值
        :return: 返回存放该标签的ResultSet类型数据, 如果请求出错, 则页面数据返回None
        '''

        bytesData = self.getHtmlMsg(strUrl)

        if bytesData is not None:
            beautifulObj = BeautifulSoup(bytesData, "html.parser")
            resultSetLabel = beautifulObj.findAll('div', {'class': strValue})
        else:
            print('请求的页面[strUrl=' + strUrl + ']数据为None')
            resultSetLabel = None

        return resultSetLabel

    def getDivLabelByClassValueOnData(self, data, strValue):

        '''
        describe: 获取div标签, 在已有的页面数据基础上,根据div标签中的class属性值来在规定页面获取
        :param data: 页面的数据, 可为bytes类型,和str类型
        :param strValue: div标签中的class属性的值
        :return: 返回存放该标签的ResultSet类型数据
        '''

        if data is not None:
            beautifulObj = BeautifulSoup(data, 'html.parser')
            resultSetLabel = beautifulObj.find_all('div', class_=strValue)

            print('爬取到[div]的标签如: ' + str(resultSetLabel))
        else:
            print('传入的[data=None], 结果为None')
            resultSetLabel = None
        return resultSetLabel

    def getLabelByText(self, strUrl, strLabelName, strText):

        '''
        describe: 根据标签的名字和标签的内容值来在规定的url页面中获取需要的标签
        :param strUrl: 需要打开的页面路径
        :param strLabelName: 需要获取的标签名字
        :param strText: 标签里面的内容
        :return: 返回一个存放标签的ResultSet类型数据
        '''

        bytesData = self.getHtmlMsg(strUrl)

        if bytesData is not None:
            beautifulObj = BeautifulSoup(bytesData, "html.parser")
            resultSetLabel = beautifulObj.find_all(strLabelName, text=strText)

            print('爬取[text=' + strText + ']的[' + strLabelName + ']标签如: ' + str(resultSetLabel))
        else:
            print('请求的页面[strUtl=' + strUrl + ']数据为None, 结果为空')
            resultSetLabel = None

        return resultSetLabel


    def getLabelByTextOnData(self, data, strLabelName, strText):

        '''
        describe: 在已有的页面数据基础上, 根据标签的名字和标签的内容值来获取标签
        :param data: bytes类型的页面数据, 也可为str类型
        :param strLabelName: 需要获取的标签名
        :param strText: 需要获取的标签的内容值
        :return: 返回一个存放标签的ResultSet类型数据
        '''
        if data is not None:
            beautifulObj = BeautifulSoup(data, "html.parser")
            resultSetLabel = beautifulObj.find_all(strLabelName, text=strText)

            print('爬取到[text=' + strText + ']的[' + strLabelName + ']标签如: ' + str(resultSetLabel))

        else:
            print('传入的[data=None], 结果为None')
            resultSetLabel = None
        return resultSetLabel

    def getLabelByKeyValueOnData(self, data, strLabelName, strKey, strValue):

        '''
        describe: 在已有的页面数据基础上, 根据标签的名字和标签的属性及属性值来获取标签, 只会获取一个, 所以要求参数值是页面中的唯一
        :param data: 页面数据, 可为bytes, str类型
        :param strLabelName: 需要获取的标签名
        :param strKey: 需要获取的标签的属性名
        :param strValue: 需要获取的标签的属性名的值
        :return: 返回一个bs4.element.Tag类型的数据
        '''
        if data is not None:
            beautifulObj = BeautifulSoup(data, "html.parser")
            tagLabel = beautifulObj.find(strLabelName, {strKey: strValue})

            print('爬取到[' + strKey + '=' + strValue + ']的[' +
                                      strLabelName + ']标签如: ' + str(tagLabel))
        else:
            print('传入的[data=None], 结果为None')
            tagLabel = None

        return tagLabel


    def getLabelByKeyValueAndBrotherOnData(self, data, strLabelName, strKey, strValue):

        '''
        describe: 在已有的页面数据基础上, 根据标签的名字和标签的属性及属性值来获取标签, 只会获取一个, 所以要求参数值是页面中的唯一
        :param data: 页面数据, 可为bytes, str类型
        :param strLabelName: 需要获取的标签名
        :param strKey: 需要获取的标签的属性名
        :param strValue: 需要获取的标签的属性名的值
        :return: 返回一个bs4.element.Tag类型的数据
        '''

        if data is not None:
            beautifulObj = BeautifulSoup(data, "html.parser")
            resultSetLabel = beautifulObj.find_previous_siblings(strLabelName, {strKey: strValue})

            print('爬取到[' + strKey + '=' + strValue + ']的[' +
                                      strLabelName + ']标签如: ' + str(resultSetLabel))

        else:
            print('传入的[data=None], 结果为None')
            resultSetLabel = None

        return resultSetLabel


    def getLabelByMoreKeyValueOnData(self, data, strLabelName, **kwargs):

        '''
        describe: 在已有的页面数据基础上, 根据标签的名字和多个标签的属性及属性值来获取标签(目前不支持class 和text, 暂时废弃)
        :param data: 页面数据, 可为bytes, str类型
        :param strLabelName: 需要获取的标签名
        :param kwargs: 键值对类型数据, 如, class='xxx', title='xxx'
        :return: 返回一个存放标签的resultSet类型数据
        '''

        if data is not None:

            beautifulObj = BeautifulSoup(data, "html.parser")
            resultSetLabel = beautifulObj.find_all(strLabelName, kwargs)

            print('爬取到[kwargs=' + str(kwargs) + ']的[' + strLabelName + ']标签如: ' + str(resultSetLabel))
        else:
            print('传入的[data=None], 结果为None')
            resultSetLabel = None

        return resultSetLabel



    def getLabelKeyValue(self, strUrl, strLabelName, strText, strKey):

        '''
        describe: 在规定的页面里, 根据标签名和标签的内容值, 来获取该标签所含有的属性的值
        :param strUrl: 页面url
        :param strLabelName: 标签名
        :param strText: 标签的内容值
        :param strKey: 需要获取的标签中的属性的名字
        :return: 返回标签中的该属性的值, 为str类型数据
        '''

        print('正在爬取[ strText=' + strText + ' ]的标签strKey=' + strKey + '的值....')

        strValue = ''
        resultSetLabel = self.getLabelByText(strUrl, strLabelName, strText)

        for Tagitem in resultSetLabel:
            strValue = Tagitem.get(strKey)

        print('爬取完成,[' + strKey + ']的值为' + strValue)
        return strValue


    def getLabelKeyValueOnData(self, data, strLabelName, strText, strKey):

        '''
        describe: 在已知的页面数据中, 根据标签名和标签的内容值, 来获取该标签所含有的属性的值
        :param data: 已知的页面数据, bytes类型或str类型
        :param strLabelName: 标签名
        :param strText: 标签的内容值
        :param strKey: 需要获取的标签中的属性的名字
        :return: 返回标签中的该属性的值, 为str类型数据
        '''

        if data is not None:
            print('正在从页面内容中解析爬取[strText=' + strText + ']的标签strKey=' + strKey + '的值....')

            intIndexTime = time.time()

            strValue = ''
            resultSetLabel = self.getLabelByTextOnData(data, strLabelName, strText)

            for Tagitem in resultSetLabel:
                strValue = Tagitem.get(strKey)

            print('爬取完成,[' + strKey + ']的值为' + strValue +
                                      '---耗时: ' + str(round(time.time() - intIndexTime, 4)) + 's')
        else:
            print('传入的[data=None], 结果为None')
            strValue = None

        return strValue