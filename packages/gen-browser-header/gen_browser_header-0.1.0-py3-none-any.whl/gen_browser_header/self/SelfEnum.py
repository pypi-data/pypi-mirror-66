#! /usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'zwzw911'

from enum import Enum, unique
@unique
class ChromeType(Enum):
    Stable = 0  #稳定版
    Beta = 1    #测试版
    Dev = 2      #开发版
    Canary = 3  #金丝雀版
    All = 4     #所有版本

@unique
class OsType(Enum):
    Win32 = 0
    Win64 = 1
    All = 2

@unique
class BrowserType(Enum):
    FireFox = 0
    Chrome = 1
    All = 2

# print(set(BrowserType.__members__.values()))
# print({BrowserType.FireFox, BrowserType.Chrome})
# a={OsType.Win64, OsType.Win32}
# print(OsType.__name__)
# print(type(OsType))
# print(type(OsType.Win64))
# print(type(OsType.Win32.name))
# print(OsType.Win32.name)
