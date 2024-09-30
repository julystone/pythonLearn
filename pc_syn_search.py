# encoding: utf-8
import json
import random
import threading
import time
from functools import wraps

import aiohttp
import requests
from Utils import DataUtil


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


class Search:
    def __init__(self, word):
        self.word = word
        self.res = None

        self.get_res()

    def get_res(self):
        data = {
            "word": self.word
        }

        h = {
            'Connection': "keep-alive",
            'User-Agent': "Mozilla/5.0",
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cookie': "*",
        }

        url = 'https://news.epolestar.xyz/flask/search/search/'
        # url = 'http://192.168.20.108:5000/search/search/'

        method = 'POST'

        syn_test = HttpRequestNoCookie()
        self.res = syn_test.request(method=method, url=url, json=data, headers=h)
        # if json.loads(self.res)['ErrorCode'] != 0:
        #     print(self.res)
        # self.res = json.dumps(json.loads(self.res)["Data"], sort_keys=True, indent=4, ensure_ascii=False)


def worker():
    OBJ = DataUtil.ReadExcel("./SearchWords/SearchWords.xlsx")
    k = 2
    write_data_list = []
    for single in OBJ.read_data_obj():
        start_time = time.time()  # 获取开始时间
        search_result = Search(single.key0).res
        end_time = time.time()  # 获取结束时间
        execution_time = round((end_time - start_time), 6)
        result_size = len(json.loads(search_result)['Data']['result'])
        print(f"{single.id} search for {single.key0} Took {execution_time}, size = {result_size}")
        write_data_list.append((result_size, execution_time, search_result))
    for i in OBJ.read_data_obj():
        OBJ.w_data_origin(row=i.row, column=3 + k * 4, data=write_data_list[i.row - 2][0])
        OBJ.w_data_origin(row=i.row, column=4 + k * 4, data=write_data_list[i.row - 2][1])
        OBJ.w_data_origin(row=i.row, column=5 + k * 4, data=write_data_list[i.row - 2][2])
    OBJ.save()


def perform_stress_test(queries, num_threads):
    results = []
    threads = []

    # 分配查询给线程
    for i in range(num_threads):
        # 创建并启动线程
        query = random.choice(queries)
        t = threading.Thread(target=worker, args=(query, results), name=f"Thread-{i + 1}")
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    print("All searches completed.")


# 示例使用
if __name__ == "__main__":
    queries = ["sc", "sr", "pp", "cj", "m2", "sh41", "au24", "cu", "SC", ""]
    num_threads = 10
    worker()
