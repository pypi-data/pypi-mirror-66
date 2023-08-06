# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-03-06 23:17:54
@LastEditTime: 2020-04-25 22:22:28
@LastEditors: ChenXiaolei
@Description: Handler基础类
"""

# seven_framework import
from . import base


class BaseHandler(base.BaseHandler):
    """
    @description: api base handler. not session
    @last_editors: ChenXiaolei
    """

    def __init__(self, *argc, **argkw):
        """
        @description: 初始化
        @last_editors: ChenXiaolei
        """
        super(base.BaseHandler, self).__init__(*argc, **argkw)

    def write_error(self, status_code, **kwargs):
        """
        @description: 重写全局异常事件捕捉
        @last_editors: ChenXiaolei
        """
        self.logger_error.exception('error_info:')
        return self.reponse_json_error()

    def prepare(self):
        """
        @description: 置于任何请求方法前被调用
        @last_editors: ChenXiaolei
        """
        pass
