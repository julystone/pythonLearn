# encoding: utf-8

import pandas as pd
import json

from icecream import ic


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def pd_json_to_df(json_data):
    df = pd.json_normalize(json_data)
    return df

def df_rename_columns(df, columns_dict):
    df = df.rename(columns=columns_dict)
    return df

def main():
    file_path = '../tempFiles/a.json'
    # data = read_json(file_path)
    df = pd.read_json(file_path)
    # df = pd_json_to_df(data)
    columns_dict = {'commodityNo': 'CommodityId', 'commodityName': 'CommodityChsName'}
    df_renamed = df_rename_columns(df, columns_dict)
    return ic(df_renamed)

if __name__ == '__main__':
    main()
