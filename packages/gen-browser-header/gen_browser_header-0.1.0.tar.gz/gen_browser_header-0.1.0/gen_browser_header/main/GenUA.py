#! /usr/bin/env python3
# -*- coding:utf-8 -*-


import logging
import random
import datetime

from  gen_browser_header.helper import Helper as helper
import gen_browser_header.self.SelfEnum as self_enum
from gen_browser_header.setting import Setting as module_setting
import gen_browser_header.self.SelfConstant as self_constant
logging.basicConfig(level=logging.DEBUG)


def generate_firefox_ua(setting, num=None):
    '''
    生成所有firefox的UA，供选择
    :param setting: GbhSetting的实例
    :param num: 生成ua的个数。如果是None，返回所有
    :return: list
    '''
    if num is not None:
        # 如果只需要返回一个，直接生成
        if num == 1:
            return ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) \
Gecko/20100101 Firefox/74.0']

    firefox_ua = []
    # print(setting.firefox_ver)
    firefox_ver = [float(x) for x in range(setting.firefox_ver['min'],
                                           setting.firefox_ver['max'])]
    # print(firefox_ver)
    os_bit = set([])
    if self_enum.OsType.All in setting.os_type:
        os_bit = {'Win32; x32', 'Win64; x64'}
    else:
        if self_enum.OsType.Win32 in setting.os_type:
            os_bit.add('Win32; x32')
        if self_enum.OsType.Win64 in setting.os_type:
            os_bit.add('Win64; x64')

    for single_os_bit in os_bit:
        if 'Win' in single_os_bit:
            firefox_ua += ['Mozilla/5.0 (%s; %s; rv:%s) \
Gecko/20100101 Firefox/%s' % (win_ver, os_info, f_ver, f_ver)
                           for win_ver in setting.WIN_VER
                           for os_info in os_bit
                           for f_ver in firefox_ver]
        else:
            raise Exception('当前不支持产生非Windows的user-agent')

    if num is not None:
        if len(firefox_ua) > num:
            return random.sample(firefox_ua, num)

    return firefox_ua


def generate_chrome_url_base_on_type(setting):
    '''
    chrome的版本需要从网页读取，结果如https://www.chromedownloads.net/chrome-win32-stable
    :param setting: GbhSetting的实例,
    :return: set，包含需要获取版本的url
    '''
    # # 检测传入参数的类型
    # if not helper.match_expect_type(os_type, 'set'):
    #     raise ValueError('generate_chrome_url_base_on_type的参数os_type，不是set')
    # if not helper.match_expect_type(chrome_type, 'set'):
    #     raise ValueError('generate_chrome_url_base_on_type的参数chrome_type，不是set')
    #     # 检测传入参数是否符合enum定义
    #     for single in os_type:
    #         if single not in self_enum.OsType:
    #             raise ValueError(
    #                 'generate_chrome_url_base_on_type的参数os_type，元素不是OsType')
    #
    #     for single in chrome_type:
    #         if single not in self_enum.ChromeType:
    #             raise ValueError('generate_chrome_url_base_on_type的参数chrome_type\
    # ,元素不是ChromeType')
    # print(setting.chrome_type)
    # if self_enum.ChromeType.All in setting.chrome_type:
    #     setting.chrome_type = {self_enum.ChromeType.Stable,
    #                            self_enum.ChromeType.Beta,
    #                            self_enum.ChromeType.Dev,
    #                            self_enum.ChromeType.Canary}
    # if self_enum.OsType.All in setting.os_type:
    #     setting.os_type = {self_enum.OsType.Win32, self_enum.OsType.Win64}
    # print(setting.chrome_type)
    # enum对应的字符
    os_dict = {
        self_enum.OsType.Win32: 'chrome32win',
        self_enum.OsType.Win64: 'chrome64win'
    }

    base_url = 'https://www.chromedownloads.net/'
    result = []
    for single_os_type in setting.os_type:
        for single in setting.chrome_type:
            part_url = os_dict[single_os_type] + '-' + single.name.lower()
            result.append(base_url + part_url)

    return result


def get_chrome_ver(setting, url):
    '''
    :param setting: setting的实例
    :param url: 获取chrome版本的url
    :return: set
    '''
    chrome_ver = set({})
    current_year = datetime.date.today().year
    # print(current_year)
    if_need_proxy = helper.detect_if_need_proxy(url)
    # print(if_need_proxy)
    valid_proxies = None
    if if_need_proxy:
        if setting.proxies is None:
            raise Exception("setting没有设置任何代理，无法连接到https://www.chromedownloads\
.net获得chrome版本")
    # print(setting.proxies)

        for single_proxies in setting.proxies:
            tmp = helper.detect_if_proxy_usable(proxies=single_proxies, url=url)
            # print(tmp)
            if tmp:
                # print(single_proxies)
                valid_proxies = single_proxies
                break

        if valid_proxies is None:
            raise Exception('尝试了所有代理，都无法连接https://www.chromedownloads.net')
    # print(valid_proxies)
    r = helper.send_request_get_response(url=url, if_use_proxy=if_need_proxy,
                                            proxies=valid_proxies,
                                            header=self_constant.HEADER)
    # print(soup)
    records = r.html.find('div.download_content>ul.fix>'
                          'li[class!=divide-line]', first=False)

    for single_record in records:
        # print(single_record.text)
        version_element_list = single_record.find('span.version_title>a')
        release_data_element_list = single_record.find(
            'span.release_date')
        # 第一个li是标题，需要忽略
        if len(version_element_list) == 0:
            continue
        # 判断版本时间
        version_release_year = \
            int(release_data_element_list[0].text.split('-')[0])
        if current_year - version_release_year + 1 > \
                setting.chrome_max_release_year:
            continue

        chrome_ver.add(version_element_list[0].text.split('_')[3])
    return chrome_ver


def generate_chrome_ua(setting, num=None):
    '''
    :param setting: setting的实例
    :param num: 期望生成chrome_ua的个数
    :return: list，包含需要获取版本的UA
    '''
    if num is not None:
        # 如果只需要返回一个，直接生成
        if num == 1:
            return ['Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36']

    try:
        version_url = generate_chrome_url_base_on_type(setting)
    except ValueError as e:
        # print('generate_chrome_header调用generate_chrome_url_base_on_type'
        #       '，传入的参数必须是set')
        print(e)
        return

    # 检测是否需要代理，如果需要，设置代理
    # if_use_proxy = helper.detect_if_need_proxy(version_url[0])
    # print(version_url)
    chrome_ver = set({})
    for single_url in version_url:
        tmp_chrome_ver = get_chrome_ver(url=single_url, setting=setting)
        # logging.debug(tmp_chrome_ver)
        # 获得的version加入chrome_ver
        chrome_ver = chrome_ver | tmp_chrome_ver
    # logging.debug(chrome_ver)
    os_bit = set([])
    if self_enum.OsType.All in setting.os_type:
        os_bit = {'Win32; x32', 'Win64; x64'}
    else:
        if self_enum.OsType.Win32 in setting.os_type:
            os_bit.add('Win32; x32')
        if self_enum.OsType.Win64 in setting.os_type:
            os_bit.add('Win64; x64')
    # os_bit = set()
    # if self_enum.OsType.All in setting.os_type:
    #     os_bit = {32, 64}
    #
    # if self_enum.OsType.Win32 in setting.os_type:
    #     os_bit.add(32)
    # if self_enum.OsType.Win64 in setting.os_type:
    #     os_bit.add(64)
    # logging.debug(os_bit)
    # for single_os_bit in os_bit:
    # if 'Win' in single_os_bit:
    # Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36
    chrome_ua = ['Mozilla/5.0 (%s; %s) AppleWebKit/537.36 (KHTML, \
like Gecko) Chrome/%s Safari/537.36' %
                 (winver, osbit, chromever)
                 for osbit in os_bit
                 for winver in setting.WIN_VER
                 for chromever in chrome_ver
                 ]
    # else:
    #     raise Exception('当前不支持产生非Windows的user-agent')

    if num is not None:
        if len(chrome_ua) > num:
            return random.sample(chrome_ua, num)

    return chrome_ua

    # return result


if __name__ == '__main__':
    try:
        # print(datetime.datetime.now())
        # print(module_setting.GbhSetting['WIN_VER'])
        cur_setting = module_setting.GbhSetting()
        cur_setting.proxy_ip = ['10.11.12.13:9090']
        # print(cur_setting.proxy_ip)
        cur_setting.firefox_ver = {'min': 74, 'max': 75}
        cur_setting.os_type = {self_enum.OsType.Win64}
        cur_setting.chrome_type = {self_enum.ChromeType.Stable}
        cur_setting.chrome_max_release_year = 1
        # print(cur_setting.firefox_ver)
        result = generate_chrome_ua(setting=cur_setting)

        # result += generate_firefox_ua(setting=cur_setting)
        print(result)
        # print(generate_chrome_url_base_on_type(setting=cur_setting))
    except Exception as e:
        print(e)
