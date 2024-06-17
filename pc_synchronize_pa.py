import random
import string
from datetime import datetime

import requests
import json


class HttpRequestNoCookie:
    def __init__(self):
        pass

    @staticmethod
    def request(method, url, data=None, params=None, json=None, headers=None, cookies=None, timeout=None):
        if method.lower() == 'get':
            res = requests.get(url=url, params=params, headers=headers, cookies=cookies, timeout=timeout)
        elif method.lower() == 'post':
            if json:
                res = requests.post(url=url, json=json, headers=headers, cookies=cookies, timeout=timeout)
            else:
                res = requests.post(url=url, data=data, headers=headers, cookies=cookies, timeout=timeout)
        else:
            res = None
        if res.status_code == 404:
            raise RuntimeError
        return res.text


class Synchronize:
    def __init__(self, userNo, source, dataType, device):
        self.userNo = userNo
        self.source = source
        self.dataType = dataType
        self.captcha, self.time_str = self.create_captcha()
        self.device = device

        self.data_str = "Self" if dataType == 1 else "Setting"
        self.device_str = "And" if device == 1 else "iOS"
        self.res = None
        self.out = None
        self.get_res()

    @staticmethod
    def create_captcha() -> tuple:
        # 1. 随机生成10位的字符串（包含大小写字母和数字）
        captcha_chars = string.ascii_letters + string.digits  # 包含大小写字母和数字的字符集
        captcha = ''.join(random.choices(captcha_chars, k=10))

        # 2. 获取当前时间并格式化为字符串
        now = datetime.now()
        time_str = now.strftime("%Y%m%d%H%M%S")

        # 3. 计算基于验证码和时间戳的某种值（这里简化为验证码字符的ASCII码之和）
        # 注意：这里不直接使用时间字符串的字符作为索引，因为长度可能不匹配
        sum_value = 0
        for index in time_str:
            sum_value += ord(captcha[ord(index) - ord('0')])
        # sum_value = sum(ord(char) for char in captcha)  # 累加验证码字符的ASCII码
        sum_str = str(sum_value)[-3:].zfill(3)  # 取最后三位，不足则补零

        # 返回完整的验证码字符串
        return captcha + time_str + sum_str, time_str

    def get_res(self):
        data = {
            "userNo": self.userNo,
            "source": self.source,
            "dataType": self.dataType,
            "captcha": self.captcha
        }

        h = {
            'Connection': "keep-alive",
            'User-Agent': "Mozilla/5.0",
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cookie': "*",
        }

        url = 'https://news.epolestar.xyz/flask/terminal/auth/server/'

        method = 'POST'

        self.res = HttpRequestNoCookie.request(method=method, url=url, json=data, headers=h)

    def common_get(self):
        self.out = json.dumps(json.loads(self.res), sort_keys=True, indent=4, ensure_ascii=False)

    def setting_analyze_get(self):
        if self.dataType == 1:
            self.out = "Param Error：Not setting type"
            return
        self.out = json.dumps(json.loads(self.res)["Data"]["SettingsConfig"]["EsKLineAnalysisLines"],
                                     sort_keys=True,
                                     indent=4, ensure_ascii=False)

    def setting_without_header(self):
        if self.dataType == 1:
            self.out = "Param Error：Not setting type"
            return
        data = json.loads(self.res)["Data"]["SettingsConfig"]
        ok = {}
        for key in data:
            if "Header" in key or "|" in key:
                continue
            ok[key] = data[key]
        self.out = json.dumps(ok, sort_keys=True, indent=4, ensure_ascii=False)

    def write_file(self):
        with open(f'./tempFiles/{self.time_str[4:]}_{self.userNo}_{self.device_str}_{self.data_str}.txt',
                  mode='w+') as f:
            f.write(self.out)


if __name__ == '__main__':
    userNo = "ESTEST015"
    source = 1              # 1:App, 2:PC
    dataType = 2            # 1:self,2:setting

    device = 1              # 1:And, 2:iOS

    out = Synchronize(userNo, source, dataType, device)
    out.setting_without_header()
    out.write_file()
