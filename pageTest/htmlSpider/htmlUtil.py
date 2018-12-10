#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-12-05 18:15


from bs4 import BeautifulSoup

class HtmlUtil:

    def getHtmlEncode(self, data):

        '''
        describe: 获取网页的编码
        :param data: 网页内容, 可string, 可bytes
        :return:
        '''
        strEncode = None
        if data is not None:

            beautifulObj = BeautifulSoup(data, "html.parser")
            tagLabel = beautifulObj.find('meta', charset=True)

            if tagLabel is not None:
                strEncode = tagLabel['charset']
        else:
            print('参数[data=None]')

        return strEncode
