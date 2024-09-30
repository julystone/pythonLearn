import random
import string
from datetime import datetime

import requests
import json
from faker import Faker


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


userNo = "ESTEST015"
source = 1  # 1:App, 2:PC
dataType = 1  # 1:self,2:setting
captcha, time_str = create_captcha()

device = 2  # 1:And, 2:iOS
data_str = "Self" if dataType == 1 else "Setting"
device_str = "And" if device == 1 else "iOS"

faker = Faker()

data = {
    "source": random.choices(['Android', 'iOS', 'PC'])[0],
    "topic": "Quote",
    "packageNo": f'000{faker.random_number(digits=3, fix_len=True)}',
    "productVer": "3.6.10",
    "productInfo": "Yi Star",
    "localTime": faker.date_time().__str__(),
    "hostName": "comdg01150023",
    "macAddr": faker.mac_address().__str__(),
    "systemInfo": "Android:14",
    "uuid": faker.uuid4().__str__(),
    "loginApi": "DipperTradeApi",
    "addrName": "北斗星(仿真)",
    "ServerIp": faker.ipv4().__str__(),
    "ServerPort": faker.port_number().__str__(),
    "addrNo": "T DIPPER 007",
    "companyNo": faker.random_number(digits=4, fix_len=True).__str__(),
    "companyName": "易盛外盘",
    "userNo": "HCC",
}
print(data)

h = {
    'Connection': "keep-alive",
    'User-Agent': "Mozilla/5.0",
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cookie': "*",
}

# url = 'https://news.epolestar.xyz/flask/terminal/server/'
url = 'https://news.epolestar.xyz/flask/terminal/behavior/add/'

method = 'POST'


def FakerOne():
    faker = Faker('zh_CN')
    res = faker.date_time().__str__()
    res1 = f'000{faker.random_number(digits=3, fix_len=True)}'
    print(res)


if __name__ == '__main__':
    res = HttpRequestNoCookie.request(method=method, url=url, json=data, headers=h)
    print(res)
    # data = json.loads(res)["Data"]["SettingsConfig"]
    out = json.dumps(json.loads(res), sort_keys=True, indent=4, ensure_ascii=False)
    print(out)
    # with open(f'./tempFiles/{device_str}_{data_str}_{userNo}_{time_str[4:]}.txt', mode='w+') as f:
    # f.write(out)
    # f.write(out)
    # f.write(analysis)
    FakerOne()
