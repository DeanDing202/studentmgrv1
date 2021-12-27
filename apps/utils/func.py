# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2021/12/10 13:17
# @Author    : Dean-kexiang Ding
# @Email     : Dean-kexiang.ding@cn.abb.com
# @File	     : func.py
# @Software  : PyCharm
# -----------------------------------------
import re

def is_Chinese(text):
    '''判断text是否有汉字'''
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    for ch in text:
        match = zhPattern.search(ch)
        if match:
            return True
    return False

def is_SpecChar(text):
    '''特殊字符判断（包括中文汉字）'''
    match = re.match("[a-zA-Z0-9]*$",text)
    if match:
        return False
    else:
        return True

# while True:
#     a = input("请输入字符：")
#     print(is_SpecChar(a))