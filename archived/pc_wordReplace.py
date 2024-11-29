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
    ic(string)

def rename(mapping, df):
    # 假设这是您的字典
    mapping = {
        '旧键1': '新键1',
        '旧键2': '新键2',
        # ...其他映射
    }

    # 您的DataFrame
    df = pd.DataFrame({
        '旧键1': [1, 2, 3],
        '旧键2': [4, 5, 6],
        # ...其他列
    })

    # 使用rename()方法进行替换
    df_renamed = df.rename(columns=mapping)
    return df_renamed


if __name__ == '__main__':
    excel_path = '../ExcelFiles/new.xlsx'
    wordsGet(excel_path)
