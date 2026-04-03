import time
import json
from enum import IntEnum, unique, auto

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from Utils.CaptchaUtil import create_captcha
from Utils.HttpUtil import HttpRequestNoCookie


@unique
class NewsType(IntEnum):
    Observer = auto()
    Goods = auto()


class UploadWeb:
    def __init__(self, url, type1):
        self.url = url
        self.type = type1
        self.res = None
        self.out = None
        # self.init()
        self.upload_web()

    def init(self):
        self.login()

    def login(self):
        json_login = {
            "LoginNo": "july",
            "LoginPwd": "A5ZjMARUYe0Q79yHkXkl/xTQDk7hl/raJV6SXf90Zsq6iqQ37qTeKZXoI8NlCtyhKC+7yMyYRIXiB+mBMWxGGwxhTM2BThh1n/MO/ReKN7NvvHbmTZoxqCh9PmTIJdjbKORLthcGl2DsIhENk3ALnwgQ3/+3QqoHTgi/nZUXBuI="
        }

        h = {
            'Connection': "keep-alive",
            'User-Agent': "Mozilla/5.0",
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cookie': "*",
        }

        url = 'http://192.168.40.38:5001/login'

        method = 'POST'

        res = HttpRequestNoCookie.request(
            method=method, url=url, json=json_login, headers=h)
        print(res)

    def upload_web(self):
        data = {
            "url": self.url,
            "type": self.type,
            "enable": 1,
        }

        h = {
            'Connection': "keep-alive",
            'User-Agent': "Mozilla/5.0",
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cookie': "*",
        }

        # url = 'http://192.168.40.38:5001/subfunction/marketdata/upload'
        url = 'http://222.88.33.249:8888/flask/subfunction/marketdata/upload'

        method = 'POST'

        self.res = HttpRequestNoCookie.request(
            method=method, url=url, data=data, headers=h)
        print(self.res)
        error_code = json.loads(self.res).get("ErrorCode", {})
        if error_code == 0 or {}:
            time.sleep(10)


def get_data(filename):
    from Utils.Excelize import ReadExcel
    res = ReadExcel(filename).read_data_obj()
    return res


def control_data(filename):
    data_sets_raw = get_data(filename)
    for obj in data_sets_raw:
        url = obj.url
        type1 = obj.type
        out = UploadWeb(url, type1)
        time.sleep(1)


if __name__ == '__main__':
    Excel_file = r"C:\Users\july4\PycharmProjects\pythonLearn\ExcelFiles\wechat_link_test.xlsx"
    control_data(Excel_file)
