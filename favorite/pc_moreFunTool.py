import time
import pandas as pd
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


def control_data(filename):
    df_raw = pd.read_json(filename)
    print(df_raw)
    df_raw.to_csv('test_moreFun.csv')

def control_data_normalize(filename):
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)  # 转换为字典列表

    # 展平嵌套字段
    df_raw = pd.json_normalize(
        data
    )

    print(df_raw)
    # df_unique = df_raw.drop_duplicates(subset=["localized.zh.name"], keep="first", inplace=False, ignore_index=False)
    df_raw.to_csv('test_moreFun_normalize_unique.csv')


if __name__ == '__main__':
    Json_file = r"C:\Users\july4\PycharmProjects\pythonLearn\ExcelFiles\personalities.json"
    control_data_normalize(Json_file)
