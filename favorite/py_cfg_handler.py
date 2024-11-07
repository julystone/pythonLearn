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

import re

from icecream import ic

class Commodity:
    def __init__(self, commodity_id, price_tick, cover_mode, commodity_type, external_commodity_no, template_no,
                 price_deno, commodity_chsname):
        self.CommodityId = commodity_id
        # self.PriceTick = float(price_tick)
        self.PriceTick = price_tick
        self.CoverMode = cover_mode
        # self.CommodityType = int(commodity_type)
        self.CommodityType = commodity_type
        self.ExternalCommodityNo = external_commodity_no
        self.TemplateNo = template_no
        # self.PriceDeno = int(price_deno)
        self.PriceDeno = price_deno
        self.CommodityChsName = commodity_chsname


def parse_config(config_text):
    commodities = []
    pattern = re.compile(r'Commodity(\d+)\.([^=]+)=(.*)')
    matches = pattern.findall(config_text)

    for match in matches:
        index, key, value = match
        index = int(index)  # Convert to 0-based index
        if index >= len(commodities):
            commodities.append(Commodity(None, None, None, None, None, None, None, None))
        setattr(commodities[index], key, value)

    return commodities


# 假设你的配置文件内容存储在一个字符串中，这里我们直接使用你提供的文本
with open("../tempFiles/CommodityApp.cfg", "r", encoding="utf-8") as f:
    config_text = f.read()

# 解析配置文件并创建Commodity对象列表
commodities = parse_config(config_text)

# 打印结果检查
# for index, commodity in enumerate(commodities):
#     print(f"Commodity{index + 1}:")
#     for attr in vars(commodity):
#         print(f"    {attr}: {getattr(commodity, attr)}")

import pandas as pd

columns = [
    'CommodityId',
    'CommodityChsName',
    'PriceTick',
    'CoverMode',
    'CommodityType',
    'ExternalCommodityNo',
    'TemplateNo',
    'PriceDeno',
]

# 创建一个空的DataFrame
df = pd.DataFrame(columns=columns)

# 遍历Commodity对象列表，并将属性值添加到DataFrame中
for index, commodity in enumerate(commodities):
    # 使用vars()函数获取对象的所有属性及其值，然后转换为字典
    row_dict = vars(commodity)
    # 将字典转换为DataFrame的一行，并添加到DataFrame中
    df = df._append(row_dict, ignore_index=True)

from py_json_handler import main

df_json = main()
df = pd.merge(df, df_json, on='CommodityId',how='left')

from Utils.Excelize import *

# 保存到Excel文件
df['PriceTick'] = df['PriceTick'].astype(float)
df['PriceDeno'] = df['PriceDeno'].astype(float)
df.to_excel("./tempFiles/CommodityApp.xlsx", index=False)


wb = ReadExcel("../tempFiles/CommodityApp.xlsx")
ws = wb.selected_sheet

column_widths = {
    'A': 30,
    'B': 30,
    'C': 10,
    'F': 30,
    'G': 20,
    'H': 10,
    'I': 30,
    'J': 10,
}
style_dict = {
    'font':
        {
            'font_size': 11,
            'font_color': 'FF0000',
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
        },
    'alignment':
        {
            'wrap_text': True,
            'shrink_to_fit': True
        }

}

width_auto_fit(ws, column_widths)
use_style_header(ws, style_dict)

wb.save()