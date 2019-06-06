#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2019-03-28 16:15

import logging
from proxyPool.util import logUtil


class ProxyPool:

    logUtil.initlog('proxyPool', 'logs')
    log_obj = logging.getLogger('proxyPool')