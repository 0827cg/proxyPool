#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-12-14 19:54


class StringUtil:

    _strSymbol = ['=', '\"', ' ', '\'']

    def remove_symbol(self, str_content):
        """
        describe: 从字符串中移除符号.
        :param str_content:
        :return:
        """
        list_new_content = []
        for strItem in list(str_content):

            if strItem not in self._strSymbol:
                list_new_content.append(strItem)
            else:
                pass
        return list_new_content

