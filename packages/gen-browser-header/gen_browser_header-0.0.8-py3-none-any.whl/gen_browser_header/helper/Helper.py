#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import chardet
import gen_browser_header.self.SelfException as self_exception
import ssl

from gen_browser_header.setting import Setting


def match_expect_type(value, expect_type):
    '''
    :param value:  待检查的值
    :param expect_type:    字符，期望的类型
    :return: Boolean
    '''
    return expect_type in str(type(value))


def all_values_preDefined(values, defined_enum):
    '''
    判断values里的值，是否都是预定义的enum
    :param values: list/set/tuple
    :param defined_enum: 自定义的enum
    :return: boolean，true：values中所有值都是预定义的，false：有非预定义的值
    '''

    def filter_func(value):
        # defined_enum.__name__  ==> enum的名字，例如OsType
        # str(type(value))       ==> 变量的类型，如果是OsType的enum，则是<enum 'OsType'>
        return '' if defined_enum.__name__ in str(type(value)) else 'False'

    r = set(filter(filter_func, values))
    # print(r)
    return len(r) == 0


def detect_if_need_proxy(url):
    # header = gen_header.gen_limit_header(1)[0]

    # print(header)
    try:
        r = requests.get(url, headers=Setting.GbhSetting.HEADER, timeout=10)
    except requests.exceptions.ConnectTimeout as e:
        print('不通过代理发起的请求超时，需要使用代理')
        return True
    return False


def detect_if_proxy_usable(proxies, timeout=5, url='https://www.baidu.com'):
    # header = gen_header.gen_limit_header(1)[0]
    # print('detect_if_proxy_usable')
    # print(setting.GbhSetting.HEADER)
    # print(proxies)
    # print(url)
    try:
        # ssl._create_default_https_context = ssl._create_unverified_context
        # print('start')
        requests.get(url, headers=Setting.GbhSetting.HEADER,
                     proxies=proxies, timeout=timeout)
        # print('in')
    except requests.exceptions.ConnectTimeout as e:
        print('代理无效')
        return False
    except requests.exceptions.ProxyError as e:
        print('代理无效')
        return False
    except requests.exceptions.ConnectionError as e:
        print('代理无效')
        return False
    return True


def send_request_get_response(*, url, if_use_proxy, proxies, header):
    '''
    :param url:
    :param if_use_proxy:  boolean
    :param proxies: dict，如果if_need_proxy为true，传入代理
    :param header: request的header
    :return: root soup
    '''
    ssl._create_default_https_context = ssl._create_unverified_context
    if if_use_proxy:
        r = requests.get(url, headers=header, proxies=proxies,
                         timeout=5)
        # verify = False
    else:
        r = requests.get(url, headers=header, timeout=2)

    if r.status_code != 200:
        print('错误代码 %s' % r.status_code)
        raise self_exception.ResponseException(r.status_code)

    # raise e.ResponseException(200)
    # logging.debug(chardet.detect(r.content)['encoding'])
    # logging.debug(r.text)
    encoding = chardet.detect(r.content)['encoding']
    if encoding == 'utf-8':
        soup = BeautifulSoup(r.text, 'lxml')
    else:
        soup = BeautifulSoup(r.text, 'lxml', from_encoding=encoding)

    return soup


def async_send_request_get_response(url, if_use_proxy, proxies, header,
                                    soup_list):
    '''
    为了使用协程（提高效率，采用异步模式：即发送request后，立刻发送下一个request，而不是等待response）
    对helper.send_request_get_response进行包装，添加一个额外参数soup_list
    ，存储beautifulsoup处理后的response
    :param url: request的地址
    :param if_use_proxy:
    :param proxies: 用来来接待代理网页的代理
    :param header:
    :param soup_list: 存储response
    :return: 无
    '''
    soup_list.append(
        send_request_get_response(url=url, if_use_proxy=if_use_proxy,
                                  proxies=proxies, header=header)
    )


if __name__ == '__main__':
    # detect_if_need_proxy(url='')
    pass
