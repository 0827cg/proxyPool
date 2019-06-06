#!/usr/common/env python3
# -*- coding: utf-8 -*-
#

# describe: 日志工具, 如若项目中需要使用到logging这个模块, 则可以使用此模块, 免去配置, 只需要传入日志文件信息即可
# 方式: 在项目入口中, 引入logging和此模块, 传入需要的参数, 如
# import logging
# import logUtil // 需是同文件夹下
# logUtil.initLog(project_name, dir_name, level)
# 然后再需要使用到日志工具的地方, 只需要键入下面的代码
# log_obj = logging.getLogger(project_name)
# 之后, 就可以使用log_obj这个对象来写入日志了, log_obj.info(xxx)...
# 日志文件名将会为strProjectName + 日期 + '.log'
# author: cg
# time: 2019-03-28 15:52


import logging
import logging.config
import logging.handlers
import os
import datetime


def initlog(project_name, dir_name, level=2):
    """
    describe: 初始化注册日志
    :param project_name: 项目名字, 也会用作日志文件的名字, 日志文件名: strProjectName + yyyy-MM-dd + '.log
    :param dir_name: 存放日志文件的文件夹名字
    :param level: 日志等级1~6, 等级越高, 打印的输出越少, 默认为2(
    0: logging.NOTSET, 1: logging.DEBUG, 2: logging.INFO, 3: logging.WARNING, 4: logging.ERROR 5: logging.CRITICAL)
    :return:
    """

    check_create_dir(dir_name)

    log_filename = project_name + '-' + str(datetime.date.today()) + '.log'
    log_level = get_log_level(level)

    logger_obj = logging.getLogger(project_name)
    logger_obj.setLevel(level)

    # format_obj = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s')

    format_obj = logging.Formatter('%(asctime)s-%(name)s-%(process)d-%(thread)d-%(threadName)s-'
                                   '%(pathname)s-%(module)s[%(funcName)s:%(lineno)d]-%(levelname)s : %(message)s')

    file_handler_obj = logging.FileHandler(dir_name + os.sep + log_filename, encoding='utf-8')

    # file_handler_obj = logging.handlers.TimedRotatingFileHandler(dir_name + os.sep + log_filename,
    # when='midnight', encoding='utf-8')

    file_handler_obj.setLevel(log_level)
    file_handler_obj.setFormatter(format_obj)

    console_handler_obj = logging.StreamHandler()
    console_handler_obj.setLevel(log_level)
    console_handler_obj.setFormatter(format_obj)

    logger_obj.addHandler(file_handler_obj)
    logger_obj.addHandler(console_handler_obj)


def check_create_dir(dir_name):
    """
    describe: 检测文件夹是否存在, 若不存在则创建
    :param dir_name: 文件夹名
    :return:
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def get_log_level(level=2):
    """
    describe: 0~5, 返回日志等级, 默认为2
    :param level: 日志等级0~5, 如不在此范围内, 则返回INFO
    :return: 日志等级, int
    """
    if level == 5:
        return logging.CRITICAL
    elif level == 4:
        return logging.ERROR
    elif level == 3:
        return logging.WARNING
    elif level == 2:
        return logging.INFO
    elif level == 1:
        return logging.DEBUG
    elif level == 0:
        return logging.NOTSET
    else:
        return logging.INFO
