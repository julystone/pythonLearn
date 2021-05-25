import json
from datetime import datetime

import requests


class HttpRequestNoCookie:
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


class EstarPost:
    def __init__(self, data, url, method='POST'):
        self.data = data
        self.url = url
        self.method = method
        self.h = {
            'Connection': "keep-alive",
            'User-Agent': "Mozilla/5.0",
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cookie': "*",
        }

    def connectJsonBeautify(self):
        res = HttpRequestNoCookie.request(method=self.method, url=self.url, json=self.data, headers=self.h)
        out = json.dumps(json.loads(res), sort_keys=False, indent=4, ensure_ascii=False)
        print(out)
        with open(f'./tempFiles/F10_{datetime.now().strftime("%H%M%S")}.txt', mode='w+') as f:
            f.write(out)


if __name__ == '__main__':
    data = {
        "Commodity": "ZCE|O|SR",
        "Language": 2052,
    }

    url = 'http://news.epolestar.xyz/flask/news/F10/'

    method = 'POST'

    estar = EstarPost(data, url, method)
    estar.connectJsonBeautify()
