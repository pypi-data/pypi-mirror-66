#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession

from bs4 import BeautifulSoup
import chardet
import gen_browser_header.self.SelfException as self_exception
import ssl

import gen_browser_header.setting.Setting as setting
import gen_browser_header.self.SelfConstant as self_constant

asession = AsyncHTMLSession()


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


def enum_set_check(value, enum_type, replace=True):
    '''
    检测value是否为set（防止重复），且其中每个值都是enum_type中成员，最后，如果有value中有all，替换所有其他成员
    :param value: 待检查的值
    :param enum_type: enum的定义
    :param replace: boolean，当value为True，是否用enum中其他所有值取代All
    :return: None（有错误）/set（原始值，或者修改过的值（All））
    '''
    # value是set
    if not match_expect_type(value, 'set'):
        # print('not set')
        return
    # value中每个值是合法的enum成员
    if not all_values_preDefined(values=value, defined_enum=enum_type):
        # print('not valid')
        return
    # value中有all，则把除all之外的成员都设置上去
    # print(enum_type['All'] in value)
    if enum_type['All'] in value:
        # print(enum_type.__members__.items())
        if replace:
            return set(
                [enum_type[k] for k, v in enum_type.__members__.items() if
                 k != 'All'])
        else:
            return {enum_type['All']}
    else:
        return value


def detect_if_need_proxy(url):
    # header = gen_header.gen_limit_header(1)[0]

    # print(header)
    try:
        # s = HTMLSession()
        HTMLSession().get(url, headers=self_constant.HEADER, timeout=10)
    except requests.exceptions.Timeout as e:
        print('不通过代理发起的请求超时，需要使用代理')
        return True
    except requests.exceptions.ConnectionError as e:
        print('不通过代理发起的请求连接错误，需要使用代理')
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

        HTMLSession().get(url, headers=self_constant.HEADER,
                          proxies=proxies, timeout=timeout)
        # print('in')
    except requests.exceptions.Timeout as e:
        print('代理无效：超时')
        return False
    except requests.exceptions.ProxyError as e:
        print('代理无效：代理错误')
        return False
    except requests.exceptions.ConnectionError as e:
        print('代理无效：连接错误')
        return False
    return True


def send_request_get_response(url, if_use_proxy, proxies, header):
    '''
    为了和async_send_request_get_response的参数保持一致，取消force_render
    :param url:
    :param if_use_proxy:  boolean
    :param proxies: dict，如果if_need_proxy为true，传入代理
    :param header: request的header
    :param force_render: 是否要进行render，默认True。如果是静态页面，无需render
    :return:
    '''
    # ssl._create_default_https_context = ssl._create_unverified_context
    if if_use_proxy:
        r = HTMLSession().get(url, headers=header, proxies=proxies,
                              timeout=5)
        # verify = False
    else:
        r = HTMLSession().get(url, headers=header, timeout=2)

    if r.status_code != 200:
        print('错误代码 %s' % r.status_code)
        raise self_exception.ResponseException(r.status_code)

    return r
    # raise e.ResponseException(200)
    # logging.debug(chardet.detect(r.content)['encoding'])
    # logging.debug(r.text)
    # encoding = chardet.detect(r.content)['encoding']
    # if encoding == 'utf-8':
    #     soup = BeautifulSoup(r.text, 'lxml')
    # else:
    #     soup = BeautifulSoup(r.text, 'lxml', from_encoding=encoding)
    # if force_render:
    #     r.html.render()
    # return r


# async def async_send_request_get_response_test(url, timeout):
#     # return await asession.get(url)
#     # r = await asession.get(url, headers=self_constant.HEADER, timeout=2)
#     return await asession.get(url, headers=self_constant.HEADER, timeout=timeout)
#     # return await r.html.render()

async def async_send_request_get_response(url, if_use_proxy=False, proxies=None,
                                          header=self_constant.HEADER):
    '''
    requests-html的异步模式下，必须返回await asession.get
    :param url: request的地址
    :param if_use_proxy:
    :param proxies: 用来来接待代理网页的代理
    :param header:
    :param force_render: 是否要进行render，默认True。如果是静态页面，无需render
    :return: 无
    '''
    if if_use_proxy:
        return await asession.get(url, headers=header, proxies=proxies,
                                  timeout=5)
        # verify = False
    else:
        return await asession.get(url, headers=header, timeout=2)

    # r = await asession.get(url, headers=header, timeout=2)
    # return r
    # if force_render:
    #     r.html.render()
    # return r


if __name__ == '__main__':
    pass
    # import gen_browser_header.setting.Setting as setting

    # r = send_request_get_response(url='https://www.baidu.com',
    #                               if_use_proxy=False, proxies={},
    #                               header=setting.GbhSetting.HEADER)
    # print(r.html.text)

    # urls = ['https://www.baidu.com', 'https://www.sina.com.cn']
    # task = []
    # for url in urls:
    #     task.append(async_send_request_get_response(url='https://www.baidu.com',
    #                                                 if_use_proxy=False,
    #                                                 proxies={},
    #                                                 header=setting.GbhSetting.HEADER,
    #                                                 force_render=True))

    # rs = asession.run(*task)
    # to=5
    # rs = asession.run(*[lambda url=url, timeout=to: async_send_request_get_response_test(url,timeout)
    #                     for url in urls])
    # # rs = asession.run(*[async_send_request_get_response_test(url='https://www.baidu.com',timeout=5)])
    # for s_r in rs:
    #     print(s_r.html.url)

    # async def get_pythonorg():
    #     r = await asession.get('https://www.sina.com.cn/')
    #     return r
    #
    #
    # async def get_reddit():
    #     r = await asession.get('https://www.baidu.com/')
    #     return r
    #
    #
    # async def get_google():
    #     r = await asession.get('https://www.sohu.com/')
    #     return r
    #
    #
    # results = asession.run(get_pythonorg(), get_reddit, get_google)
    # print(results)
