# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-03-06 23:17:54
@LastEditTime: 2020-04-25 22:20:35
@LastEditors: ChenXiaolei
@Description: Handler基础类
"""

# seven_framework import
from . import base

# third package import
from pycket.session import SessionManager


class BaseHandler(base.BaseHandler):
    """
    @description: api base handler. have session
    @last_editors: ChenXiaolei
    """

    def __init__(self, *argc, **argkw):
        """
        @description: 初始化
        @last_editors: ChenXiaolei
        """
        super(base.BaseHandler, self).__init__(*argc, **argkw)
        self.session = SessionManager(self)

    def prepare(self):
        """
        @description: 置于任何请求方法前被调用
        @last_editors: ChenXiaolei
        """
        pass

    # 根据key 获取Session 内容
    def get_session_value(self, key):
        """
        @description: 二次封装获取session，无则返回默认值
        @param key: session key
        @return: session value
        @last_editors: ChenXiaolei
        """
        if key in self.session:
            return self.session[key]
        else:
            return None
