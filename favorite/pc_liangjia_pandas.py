#  _____            ___             ____     __
# /\___ \          /\_ \           /\  _`\  /\ \__
# \/__/\ \   __  __\//\ \    __  __\ \,\L\_\\ \ ,_\    ___     ___       __
#    _\ \ \ /\ \/\ \ \ \ \  /\ \/\ \\/_\__ \ \ \ \/   / __`\ /' _ `\   /'__`\
#   /\ \_\ \\ \ \_\ \ \_\ \_\ \ \_\ \ /\ \L\ \\ \ \_ /\ \L\ \/\ \/\ \ /\  __/
#   \ \____/ \ \____/ /\____\\/`____ \\ `\____\\ \__\\ \____/\ \_\ \_\\ \____\
#    \/___/   \/___/  \/____/ `/___/> \\/_____/ \/__/ \/___/  \/_/\/_/ \/____/
#                                /\___/
#                                \/__/
# encoding: utf-8

import pandas as pd

def words_get(path):
    origin_df = pd.read_excel(path, sheet_name='Sheet1')
    return origin_df

def cal_poc(df):

    grouped = df.groupby('price')['qty'].sum()

    price_qty_dict = grouped.to_dict()

    print(price_qty_dict)
    return price_qty_dict, max(price_qty_dict, key=price_qty_dict.get)


if __name__ == '__main__':
    path = '../ExcelFiles/tick_data.xlsx'
    df = words_get(path)
    dict, poc = cal_poc(df)
    print(dict.get(2250.0))
    print(dict.get(2300.0))
    print(poc)