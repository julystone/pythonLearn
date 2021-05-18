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


data = {
    "userNo": "JULY401",
    "source": 1,
    "dataType": 2
}

h = {
    'Connection': "keep-alive",
    'User-Agent': "Mozilla/5.0",
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Cookie': "*",
}

url = 'http://news.epolestar.xyz/flask/terminal/server/'

method = 'POST'

if __name__ == '__main__':
    res = HttpRequestNoCookie.request(method=method, url=url, json=data, headers=h)
    out = json.dumps(json.loads(res), sort_keys=True, indent=4, ensure_ascii=False)
    # with open(f'./test_{datetime.now()}.txt', mode='w+') as f:
    with open(f'./test_{datetime.now().strftime("%H%M%S")}.txt', mode='w+') as f:
        f.write(out)
