# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-03-06 23:17:54
@LastEditTime: 2020-04-23 19:45:33
@LastEditors: ChenXiaolei
@Description: 数据库基础操作类
"""

from seven_framework.mysql import MySQLHelper
import datetime
import os
from seven_framework import config


class BaseModel:
    def __init__(self, model_class, sub_table):
        """
        @description: 基础数据库操作类
        @param model_class: 实体对象类
        @param sub_table: 分表标识
        @last_editors: ChenXiaolei
        """
        # 实体对象类
        self.model_class = model_class
        # 实体对象
        self.model_obj = model_class()
        # 数据库表名
        self.table_name = str(self.model_obj) if not sub_table else str(
            self.model_obj).lower().replace("_tb", f"_{sub_table}_tb")
        # 主键字段名
        self.primary_key_field = self.model_obj.get_primary_key()

    def __row_entity(self, data):
        """
        @description: 单条数据转成对象
        @param data :数据字典
        @return: 模型实体
        @last_editors: ChenXiaolei
        """
        field_list = self.model_obj.get_field_list()
        if data is None or len(field_list) == 0:
            return None
        model_entity = self.model_class()
        for field_str in field_list:
            setattr(model_entity, field_str, data[field_str])
        return model_entity

    def __row_entity_list(self, data_list):
        """
        @description: 数据列表返回对象
        @param data_list: 数据字典数组
        @return: 模型实体列表
        @last_editors: ChenXiaolei
        """
        field_list = self.model_obj.get_field_list()
        if data_list is None or len(field_list) == 0:
            return None
        model_entity_list = []
        if len(data_list) > 0:
            for data in data_list:

                model_entity = self.model_class()
                for field_str in field_list:
                    if field_str in data:
                        setattr(model_entity, field_str, data[field_str])
                model_entity_list.append(model_entity)
        return model_entity_list

    def get_list(self, condition='', params=None):
        """
        @description: 根据条件获取列表
        @param condition: 数据库查询条件语句
        @param params: 参数化查询参数
        @return: 模型实体列表
        @last_editors: ChenXiaolei
        """
        if condition and condition.strip() != '':
            condition = " WHERE " + condition
        sql = f"SELECT * FROM {self.table_name}{condition};"
        list_row = self.db.fetch_all_rows(sql, params)
        return self.__row_entity_list(list_row)

    def get_page_list(self,
                      field,
                      page_index,
                      page_size,
                      condition='',
                      params=None):
        """
        @description: 分页获取数据
        @param field: 查询字段 
        @param page_index: 分页页码 0为第一页
        @param page_size: 分页返回数据数量
        @param condition: 数据库查询条件语句
        @param params: 参数化查询参数
        @return: 模型实体列表
        @last_editors: ChenXiaolei
        """
        if condition and condition.strip() != '':
            condition = " WHERE " + condition
        sql = f"SELECT {field} FROM {self.table_name}{condition} LIMIT {str(int(page_index) * int(page_size))},{str(page_size)};"
        list_row = self.db.fetch_all_rows(sql, params)
        return self.__row_entity_list(list_row)

    def get_entity(self, condition='', params=None):
        """
        @description: 根据条件获取实体对象
        @param condition: 数据库查询条件语句
        @param params: 参数化查询参数
        @return: 模型实体
        @last_editors: ChenXiaolei
        """
        if condition and condition.strip() != '':
            condition = " WHERE " + condition
        sql = f"SELECT * FROM {self.table_name}{condition};"
        list_row = self.db.fetch_one_row(sql, params)
        return self.__row_entity(list_row)

    def get_entity_by_id(self, primary_key_id):
        """
        @description: 根据主键值获取实体对象
        @param primary_key_id: 主键ID值 
        @return: 模型实体
        @last_editors: ChenXiaolei
        """
        sql = f"SELECT * FROM {self.table_name} WHERE {self.primary_key_field}=%s;"
        list_row = self.db.fetch_one_row(sql, primary_key_id)
        return self.__row_entity(list_row)

    def get_total(self, condition='', params=None):
        """
        @description: 根据条件获取数据数量
        @param condition: 数据库查询条件语句
        @param params: 参数化查询参数
        @return: 查询符合条件的行的数量
        @last_editors: ChenXiaolei
        """
        if condition and condition.strip() != '':
            condition = " WHERE " + condition
        sql = f"SELECT COUNT(*) AS count FROM {self.table_name}{condition};"
        list_row = self.db.fetch_one_row(sql, params)
        return list_row['count']

    def del_entity(self, condition, params=None):
        """
        @description: 根据条件删除数据库中的数据
        @param condition: 数据库查询条件语句
        @param params: 参数化查询参数
        @return: 
        @last_editors: ChenXiaolei
        """
        if condition:
            condition = " WHERE " + condition
            sql = "DELETE FROM " + self.table_name + condition
            list_row = self.db.update(sql, params)
            if list_row is not None and list_row.rowcount >= 0:
                return True
            else:
                return False

    def add_entity(self, model):
        """
        @description: 数据入库
        @param model: 模型实体 
        @return: 如果主键为自增ID，返回主键值
        @last_editors: ChenXiaolei
        """
        field_list = self.model_obj.get_field_list()
        if len(field_list) == 0:
            return 0
        insert_field_str = ""
        insert_value_str = ""
        param = []
        for field_str in field_list:
            if str(field_str).lower() == self.primary_key_field:
                continue
            insert_field_str += str(field_str + ",")
            insert_value_str += "%s,"
            param.append(str(getattr(model, field_str)))
        insert_field_str = insert_field_str.rstrip(',')
        insert_value_str = insert_value_str.rstrip(',')
        sql = f"INSERT INTO {self.table_name}({insert_field_str}) VALUE({insert_value_str});"
        list_row = self.db.insert(sql, tuple(param))
        return list_row

    def add_update_entity(self, model, update_sql, params=None):
        """
        @description: 数据入库,遇到主键冲突则更新指定字段
        @param model: 模型实体 
        @param update_sql: 如果主键冲突则执行的更新sql语句
        @param params: 参数化查询参数
        @return: 如果主键为自增ID，返回主键值
        @last_editors: ChenXiaolei
        """
        field_list = self.model_obj.get_field_list()
        if len(field_list) == 0:
            return 0
        insert_field_str = ""
        insert_value_str = ""
        param = []
        for field_str in field_list:
            if str(field_str).lower() == self.primary_key_field:
                continue
            insert_field_str += str(field_str + ",")
            insert_value_str += "%s,"
            param.append(str(getattr(model, field_str)))
        insert_field_str = insert_field_str.rstrip(',')
        insert_value_str = insert_value_str.rstrip(',')
        sql = f"INSERT INTO {self.table_name}({insert_field_str}) VALUE({insert_value_str}) ON DUPLICATE KEY UPDATE {update_sql};"
        list_row = self.db.insert(sql, tuple(param))
        return list_row

    def update_entity(self, model):
        """
        @description: 根据模型的主键ID，更新字段的值
        @param model: 模型实体
        @return: 更新成功返回主键ID，否则返回空字符串
        @last_editors: ChenXiaolei
        """
        field_list = self.model_obj.get_field_list()
        if len(field_list) == 0:
            return 0
        update_field_str = ""

        param = []
        mid = ""
        for field_str in field_list:
            if self.primary_key_field and str(field_str).lower() == self.primary_key_field.lower():
                mid = getattr(model, field_str)
                continue
            update_field_str += str(field_str + "=%s,")
            if str(field_str).lower() == "edit_on":
                now = datetime.datetime.now()
                param.append(str(now.strftime("%Y-%m-%d %H:%M:%S")))
            else:
                param.append(str(getattr(model, field_str)))
        param.append(mid)
        update_field_str = update_field_str.rstrip(',')
        if mid == 0:
            return 0
        sql = f"UPDATE {self.table_name} SET {update_field_str} WHERE {self.primary_key_field}=%s;"
        data = self.db.update(sql, tuple(param))
        if data is not None and data.rowcount >= 0:
            return mid
        else:
            return ""

    def update_table(self, update_sql, condition, params=None):
        """
        @description: 更新数据表
        @param update_sql: 更新set语句
        @param condition: 数据库查询条件语句
        @param params: 参数化查询参数
        @return: 更新成功即为True 失败则为False
        @last_editors: ChenXiaolei
        """
        if condition and condition.strip() != '':
            condition = " WHERE " + condition
        sql = f"UPDATE {self.table_name} SET {update_sql}{condition};"
        data = self.db.update(sql, params)
        if data is not None and data.rowcount >= 0:
            return True
        else:
            return False

    def get_dict(self, condition, field="*", params=None):
        """
        @description: 返回字典dict
        @param condition: 数据库查询条件语句
        @param field: 查询字段 
        @param params: 参数化查询参数
        @return: 返回匹配条件的第一行字典数据
        @last_editors: ChenXiaolei
        """
        if condition and condition.strip() != '':
            condition = " WHERE " + condition
        sql = f"SELECT {field} FROM {self.table_name}{condition}"
        one_row = self.db.fetch_one_row(sql, params)
        return one_row  # self.__row_entity(list_row)

    def get_dict_by_id(self, primary_key_id, field="*"):
        """
        @description: 根据主键ID获取dict
        @param primary_key_id: 主键id值 
        @param field: 查询字段 
        @return: 返回匹配id的第一行字典数据
        @last_editors: ChenXiaolei
        """
        sql = f"SELECT {field} FROM {self.table_name} WHERE {self.primary_key_field}=%s;"
        one_row = self.db.fetch_one_row(sql, primary_key_id)
        return one_row

    def get_dict_list(self, condition, field="*", params=None):
        """
        @description: 返回字典列表dict list
        @param condition: 数据库查询条件语句
        @param field: 查询字段 
        @param params: 参数化查询参数
        @return: 
        @last_editors: ChenXiaolei
        """
        if condition and condition.strip() != '':
            condition = " WHERE " + condition
        sql = f"SELECT {field} FROM {self.table_name}{condition};"
        list_row = self.db.fetch_all_rows(sql, params)
        return list_row  # self.__row_entity_list(list_row)

    def get_dict_page_list(self,
                           field,
                           page_index,
                           page_size,
                           condition,
                           params=None):
        """
        @description: 获取分页字典数据
        @param field: 查询字段 
        @param page_index: 分页页码 0为第一页
        @param page_size: 分页返回数据数量
        @param condition: 数据库查询条件语句
        @param params: 参数化查询参数
        @return: 数据字典数组
        @last_editors: ChenXiaolei
        """
        if condition and condition.strip() != '':
            condition = " WHERE " + condition
        sql = f"SELECT {field} FROM {self.table_name}{condition} LIMIT {str(int(page_index) * int(page_size))},{str(page_size)}"
        list_row = self.db.fetch_all_rows(sql, params)
        return list_row