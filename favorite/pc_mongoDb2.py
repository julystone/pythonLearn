# -*- coding:utf-8 -*-
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from icecream import ic


def get_mongo_data():
    """
    获取MongoDB数据
    """
    from config_files.db_setting import mongoDB
    try:
        client = pymongo.MongoClient(
            f"mongodb://{mongoDB['host']}:{mongoDB['port']}/")
        uzi = client['uzi']
        user_tracking = uzi["home_page_elements"]
        return list(user_tracking.find())
    except Exception as e:
        print(f"获取MongoDB数据时出错: {e}")
        return []



def main():
    docs = get_mongo_data()
    print(docs)

if __name__ == '__main__':
    main()
