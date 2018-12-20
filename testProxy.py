#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-12-20 18:56
import time
import urllib.request
from bs4 import UnicodeDammit



class TestProxy():

    headerObj = {}
    headerObj['User-Agent'] = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
                                       '(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36')


    def getProxyHtmlHttpReponse(self, strUrl):
        '''
        describe: 请求url, 获取响应内容, 使用代理方式
        :param strUrl: 需要请求的url
        :param proxyMsgObj: 代理服务器信息
        :return: 返回一个httpResponse类型的数据, 请求出错返回None
        '''

        httpResponseData = None

        print('正在请求页面[' + strUrl + ']')

        # print('正在连接代理服务器[' + str(proxyMsgObj) + ']')

        # proxyHandlerObj = urllib.request.ProxyHandler(proxies={'https': '218.59.228.18:61976'})
        # print(type(proxyHandlerObj))
        # print(proxyHandlerObj)
        # print(str(proxyHandlerObj))

        # openerDirectorObj = urllib.request.build_opener(proxyHandlerObj)
        # print(type(openerDirectorObj))
        # print(openerDirectorObj)
        # print(str(openerDirectorObj))

        intIndexRequestTime = time.time()
        try:
            reqObj = urllib.request.Request(strUrl, headers=self.headerObj)
            reqObj.set_proxy('61.135.155.82:443', 'http')
            print(urllib.request.getproxies())
            # httpResponseData = openerDirectorObj.open(reqObj)
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


    def getProxyHtmlStrMsgNew(self, strUrl):

        '''
        describe: 根据url来获取页面的源代码内容, 这里通过使用UnicodeDammit这个模块来获取页面编码及内容
        :param strUrl: 需要获取的页面的url
        :param proxyMsgObj: 代理服务器信息
        :return: 返回页面数据, 为str类型, 如果请求出错, 则页面数据返回None
        '''

        httpResponseData = self.getProxyHtmlHttpReponse(strUrl)

        if httpResponseData is not None:

            bytesData = httpResponseData.read()

            udObj = UnicodeDammit(bytesData)
            strHtml = udObj.unicode_markup

            httpResponseData.close()
        else:
            strHtml = None
        # print(httpResponseData.closed)
        return strHtml


strUrl = 'http://2018.ip138.com/ic.asp'
strPageContent = TestProxy().getProxyHtmlStrMsgNew(strUrl)
print(strPageContent)