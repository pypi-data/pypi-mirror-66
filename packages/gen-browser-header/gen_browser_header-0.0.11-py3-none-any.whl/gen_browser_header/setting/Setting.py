#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# from src.self import SelfEnum as self_enum
import gen_browser_header.self.SelfEnum as self_enum
import gen_browser_header.helper.Helper as helper
import datetime

CHROME_MAX_RELEASE_YEAR = datetime.date.today().year - 2008 + 1

class GbhSetting(object):
    # 如果是模拟windows下浏览器产生的user-agent，那么需要模拟那些windows版本
    # 6.0 = Vista   6.1=win7    6.2=win8   6.3=win8.1   10 = win10
    WIN_VER = ['Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2',
               'Windows NT 6.3', 'Windows NT 10.0']

    # 如果只是用来判断是否需要使用代理，则无需随机生成header，使用固定的header即可
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept': 'text/html, application/xhtml+xml, application/xml;q = 0.9, image/webp, image/apng, */*;q = 0.8, application/signed-exchange;v = b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive'}

    # _proxy_ip: 默认None。设置必须是list，用来生成代理，连接到无法直连的网站
    # _firefox_header_no_ua: dict。用来生成header的模板，填入ua，即可生成header
    # _browser_type: set。产生哪些浏览器的ua，当前支持firefox和chrome
    # _firefox_ver： dict。产生的ua对应的ff的版本，有2个key，min和max
    # _chrome_type： set。chrome有4类型，stable/dev/Canary/beta，产生的ua是哪种类型
    # _chrome_max_release_year： int。产生的chrome最远是几年前（太老的版本不使用
    # _os_type: set。哪种操作系统上生成的ua。当前支持win32和win64
    __slots__ = ('_proxy_ip',  '_firefox_header_no_ua', '_chrome_header_no_ua',
                 '_browser_type', '_firefox_ver', '_chrome_type',
                 '_chrome_max_release_year', '_os_type')

    def __init__(self):
        self._proxy_ip = None
        self._firefox_header_no_ua = {
        'Accept': 'text/html, application/xhtml+xml, application/xml;q = 0.9, image/webp, image/apng, */*;q = 0.8, application/signed-exchange;v = b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive'}
        self._chrome_header_no_ua = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive'}
        # self._proxies = None
        self._browser_type = {self_enum.BrowserType.FireFox}
        self._firefox_ver = {'min': 64, 'max': 75}
        self._chrome_type = {self_enum.ChromeType.Stable}
        self._chrome_max_release_year = 2
        self._os_type = {self_enum.OsType.Win64}

    @property
    def proxies(self):
        if self._proxy_ip is None:
            # self._proxies = None
            return None
        else:
            # self._proxies = [{'http:%s' % ip, 'https:%s' % ip} for ip in self._proxy_ip]
            return [{'http':'%s' % ip, 'https':'%s' % ip} for ip in self._proxy_ip]
        # return self._proxies


    @property
    def firefox_header_no_ua(self):
        return self._firefox_header_no_ua

    @firefox_header_no_ua.setter
    def firefox_header_no_ua(self, value):
        # 偷懒，不检查格式了
        self._firefox_header_no_ua = value

    @property
    def chrome_header_no_ua(self):
        return self._chrome_header_no_ua

    @chrome_header_no_ua.setter
    def chrome_header_no_ua(self, value):
        # 偷懒，不检查格式了
        self._chrome_header_no_ua = value

    @property
    def browser_type(self):
        return self._browser_type

    @browser_type.setter
    def browser_type(self, value):
        r = helper.enum_set_check(value, self_enum.BrowserType)
        if r is None:
            return
        else:
            self._browser_type = r
        # # value是set
        # if not helper.match_expect_type(value, 'set'):
        #     # print('not set')
        #     return
        # # value中每个值是合法的browser_type
        # if not helper.all_values_preDefined(values=value,
        #                                     defined_enum=self_enum.BrowserType):
        #     # print('not valid')
        #     return
        # # value中有all，则只设置all
        # if self_enum.BrowserType.All in value:
        #     self._browser_type = {self_enum.BrowserType.Chrome,
        #                           self_enum.BrowserType.FireFox}
        #     return
        # # print(value)
        # self._browser_type = value

    @property
    def proxy_ip(self):
        return self._proxy_ip

    # chrome的版本需要连接到https://www.chromedownloads.net/来读取，如果直接连接不行，那么会采用proxy_ip
    # 中的代理进行尝试
    @proxy_ip.setter
    def proxy_ip(self, value):
        self._proxy_ip = value

    @property
    def firefox_ver(self):
        return self._firefox_ver

    @firefox_ver.setter
    def firefox_ver(self, value):
        # 如果格式不符合，保持原来的值，不做任何修改
        if not helper.match_expect_type(value, 'dict'):
            return
        if 'min' in value and helper.match_expect_type(value['min'], 'int'):
            self._firefox_ver['min'] = value['min']
        # 使用range进行list生成时，会会忽略最大值，所以需要+1
        # [range(74, 75)] => [74]
        if 'max' in value and helper.match_expect_type(value['max'], 'int'):
            self._firefox_ver['max'] = value['max']+1

    @property
    def chrome_type(self):
        return self._chrome_type

    @chrome_type.setter
    def chrome_type(self, value):
        r = helper.enum_set_check(value, self_enum.ChromeType)
        if r is None:
            return
        else:
            self._chrome_type = r
        # # value是set
        # if not helper.match_expect_type(value, 'set'):
        #     # print('not set')
        #     return
        # # value中每个值是合法的chrome_type
        # if not helper.all_values_preDefined(values=value,
        #                                     defined_enum=self_enum.ChromeType):
        #     # print('not valid')
        #     return
        # # value中有all，则只设置all
        # if self_enum.ChromeType.All in value:
        #     self._chrome_type = {self_enum.ChromeType.Stable,
        #                          self_enum.ChromeType.Beta,
        #                          self_enum.ChromeType.Canary,
        #                          self_enum.ChromeType.Dev}
        #     return
        #
        # self._chrome_type = value

    @property
    def chrome_max_release_year(self):
        return self._chrome_max_release_year

    @chrome_max_release_year.setter
    def chrome_max_release_year(self, value):
        # 是否为整数
        if not helper.match_expect_type(value, 'int'):
            return
        # 是否大于0
        if value < 0:
            return
        # 是否小于当前年-2008
        if CHROME_MAX_RELEASE_YEAR < value:
            return
        self._chrome_max_release_year = value

    @property
    def os_type(self):
        return self._os_type

    @os_type.setter
    def os_type(self, value):
        r = helper.enum_set_check(value, self_enum.OsType)
        if r is None:
            return
        else:
            self._os_type = r
        # # 必须是set，否则直接返回，保留原始设置
        # if not helper.match_expect_type(value, 'set'):
        #     return
        # # set中每个值都是self_enum.OsType中定义过的, 否则直接返回，保留原始设置
        # if not helper.all_values_preDefined(values=value,
        #                                     defined_enum=self_enum.OsType):
        #     return
        # # 如果有self_enum.OsType.ALL，则只保留ALL，其他删除
        # if self_enum.OsType.All in value:
        #     self._os_type = {self_enum.OsType.Win32, self_enum.OsType.Win64}
        #     return
        #
        # self._os_type = value



if __name__ == '__main__':

    # print(GbhSetting['WIN_VER'])
    st = GbhSetting()
    # st.browser_type = {self_enum.BrowserType.All}
    # print(st.browser_type)
    # st.chrome_type = {self_enum.ChromeType.All}
    # print(st.chrome_type)
    # st.chrome_type = {self_enum.ChromeType.Stable}
    # print(st.chrome_type)
    # st.os_type = {self_enum.OsType.All}
    # print(st.os_type)
    # st.os_type = {self_enum.OsType.Win32}
    # print(st.os_type)
    # print(st.proxy_ip)
    # print(st.proxies)
    # st.firefox_ver = {'min':72,'max':75}
    # print(st.firefox_ver)
    #
    # print(st.WIN_VER)
    # print(st.HEADER)


