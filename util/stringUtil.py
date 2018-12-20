#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-12-14 19:54


class StringUtil:

    strSymbol = ['=', '\"', ' ', '\'']

    def removeSymbol(self, strContent):

        '''
        describe: 从字符串中移除符号.
        :param strContent:
        :return:
        '''

        listNewContent = []
        for strItem in list(strContent):

            if strItem not in self.strSymbol:
                listNewContent.append(strItem)
            else:
                pass
        return listNewContent


    # def findValue(self, strContent):

