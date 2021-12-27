# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2021/12/9 10:08
# @Author    : Dean-kexiang Ding
# @Email     : Dean-kexiang.ding@cn.abb.com
# @File	     : sqlhelper.py
# @Software  : PyCharm
# -----------------------------------------
import re

import pymysql

class MysqlConn:
    '''针对MySql数据库建类'''
    def __init__(self, conn_info: dict):
        '''
        类的构造函数
        :param conn_info: 连接数据库的接口参数（settings.DATABASES里面，定义也是dict，保存一致）
        '''
        #接收数据库初始化参数
        self.conn_info = conn_info
        #准备一个集合存储最后结果
        self.result = []
        #定义个变量来标志程序执行是否成功（0->失败， 1->成功）
        self.flag = 0
        #定义异常信息存储变量
        self.msg = ""

    def get_db_data(self, sql: str):
        '''
        获取数据库表中数据，通过sql语句实现
        :param sql: 提供的sql语句
        :return: 返回的结果
        '''
        mysql_conn = '' #mysql_conn实例在程序块try外面定义，避免后面finally里面识别不到
        try:#执行可能出错的代码 ------Dean
            # 实例化一个数据库对象
            mysql_conn = pymysql.connect(host=self.conn_info['HOST'], port=self.conn_info['PORT'],
                                         user=self.conn_info['USER'], password=self.conn_info['PASSWORD'],
                                         database=self.conn_info['DB_NAME'], charset=self.conn_info['CHARSET'])
            # step_1: 定义一个指针cursor（光标）(实例化数据库对象后，根据数据库访问操作流程进行数据库操作)
            cursor = mysql_conn.cursor()
            # step_2: 准备操作数据库SQL语言
            #sql = 'SELECT SNo,SName,Gender,Birthday,Mobile,Email,Address FROM Student'
            # step_3: 执行操作数据库SQL语言
            cursor.execute(sql)
            # step_4: 从数据库中取出执行结果
            self.result = list(cursor.fetchall())#cursor.fetchall()返回的是元组，转换为list，与self.result定义类型保存一致
            self.flag = 1
            #执行完成后关闭数据库操作
            mysql_conn.close()
        except Exception as e:#执行出错后执行的代码（Exception as e => 把系统错误存放呆e）------Dean
            self.flag = 0
            self.msg = '连接数据库操作异常，具体原因：' + str(e)
        # finally:#无论对错都要执行的代码 => 通常用来关闭数据库
        #     mysql_conn.close()

    def update_db(self, sql: str):
        '''
        更新数据库 => 数据库的增删改除
        :param sql:
        :return:
        '''
        mysql_conn = '' #mysql_conn实例在程序块try外面定义，避免后面finally里面识别不到
        try:#执行可能出错的代码 ------Dean
        # 实例化一个数据库对象
            mysql_conn = pymysql.connect(host=self.conn_info['HOST'], port=self.conn_info['PORT'],
                                         user=self.conn_info['USER'], password=self.conn_info['PASSWORD'],
                                         database=self.conn_info['DB_NAME'], charset=self.conn_info['CHARSET'])
            # step_1: 定义一个指针cursor（光标）(实例化数据库对象后，根据数据库访问操作流程进行数据库操作)
            cursor = mysql_conn.cursor()
            # step_2: 准备操作数据库SQL语言
            #sql = 'SELECT SNo,SName,Gender,Birthday,Mobile,Email,Address FROM Student'
            # step_3: 执行操作数据库SQL语言
            cursor.execute(sql)
            # step_4: 提交更新数据库
            mysql_conn.commit()
            self.flag = 1
            # 执行完成后关闭数据库操作
            mysql_conn.close()
        except Exception as e:#执行出错后执行的代码（Exception as e => 把系统错误存放呆e）------Dean
            self.flag = 0
            self.msg = '连接数据库操作异常，具体原因：' + str(e)
            mysql_conn.rollback()#出错后数据库要回滚 ------Dean
        # finally:#无论对错都要执行的代码 => 通常用来关闭数据库
        #     mysql_conn.close()

class MssqlConn:
    pass

class OracleConn:
    pass

class MongDBConn():
    pass
