import random
import string
from datetime import datetime

import requests
import json
from faker import Faker
from Utils.HttpUtil import HttpRequestNoCookie
from Utils.CaptchaUtil import create_captcha

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
