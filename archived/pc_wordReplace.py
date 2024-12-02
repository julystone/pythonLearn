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
from icecream import ic


def wordsGet(excel_path):
    data1 = pd.read_excel(excel_path, sheet_name='all_json')
    data2 = pd.read_excel(excel_path, sheet_name='id_mapping')

    data2 = data2[['CommodityId', 'CommodityChsName_x']]

    ic(data2)

    string = data1['AllMap']
    rename(data2, data1)
    # ic(string)


def rename(mapping_df, df):
    mapping_df.fillna('', inplace=True)
    mapping = dict(zip(mapping_df['CommodityId'], mapping_df['CommodityChsName_x']))
    ic(mapping)

    # df['SixMap'] = df['SixMap'].str.replace(mapping)
    for key,value in mapping.items():
        ic(key, value)
        df['SixMap'] = df['SixMap'].str.replace(key, value)
        # df['SixMap'] = df['SixMap'].str.replace('123', '456')
    # df['SixMap'] = df['SixMap'].map(mapping)
    ic(df)
    return df


if __name__ == '__main__':
    excel_path = '../ExcelFiles/new.xlsx'
    wordsGet(excel_path)
