#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-12-14 19:33

class ListUtil:

    def findStr(self, listObj, strContent):

        '''
        describe: 从list中查找其元素跟strContent匹配的第一个下标, 并返回
        :param listObj: list对象
        :param strContent: 需要查找的字符串
        :return: 下标, int类型
        '''

        intResult, intIndex = -1, 0
        for strItem in listObj:
            if strItem.find(strContent) != -1:
                intResult = intIndex
                break
            intIndex += 1

        return intResult
