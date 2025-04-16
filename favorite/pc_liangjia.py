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
from math import floor

import pandas as pd

from Utils.Excelize import ReadExcel

raw_data = ReadExcel('../ExcelFiles/tick_data.xlsx')

obj = raw_data.read_data_obj()

def diff_price(max_price, min_price, keep_rate):
    diff = max_price - min_price
    length = diff/70/keep_rate
    floor_length = round(floor(length) * keep_rate, 1)
    print(floor_length)
    diff_list = []
    i_right = min_price
    while 1:
        i_left = round(i_right + floor_length,1)
        if i_left > max_price:
            break
        diff_list.append([i_right, i_left])
        i_right = round(i_left + 0.1, 1)
    diff_list.append([i_right, max_price])
    print(diff_list)
    return diff_list

def cal_buy_sell_1st(obj):
    buy_list = [[obj[0].price, obj[0].qty]]
    sell_list = []
    last_price = obj[0].price
    buy_flag = True
    for i in obj[1:]:
        if i.price > last_price:
            buy_list.append([i.price, i.qty])
            buy_flag = True
        elif i.price < last_price:
            sell_list.append([i.price, i.qty])
            buy_flag = False
        else:
            if buy_flag:
                buy_list.append([i.price, i.qty])
            else:
                sell_list.append([i.price, i.qty])
        print(i.time, i.qty, i.price, i.askPrice, i.sellPrice, buy_flag)
        last_price = i.price
    return buy_list, sell_list

def cal_buy_sell_2nd(obj):
    buy_list = []
    sell_list = []
    buy_flag = True
    for i in obj:
        if i.price >= i.sellPrice:
            buy_list.append([i.price, i.qty])
            buy_flag = True
        elif i.price <= i.askPrice:
            sell_list.append([i.price, i.qty])
            buy_flag = False
        else:
            continue
    print(buy_list, sell_list)
    return buy_list, sell_list

def buy_sell_percent(buy_list, sell_list):
    buy_sum = sum([float(i[1]) for i in buy_list])
    sell_sum = sum([float(i[1]) for i in sell_list])
    buy_percent = round(buy_sum/(buy_sum+sell_sum)*100, 1)
    print(buy_percent, buy_sum+sell_sum)

def cal_volumn_diff(obj, diff_list):
    price_intervals = [tuple(sublist) for sublist in diff_list]

    from collections import defaultdict

    temp_dict = defaultdict(list)  # 创建一个整型的默认字典，缺失的键默认为0
    for i in obj:
        for j in price_intervals:
            if j[0] <= float(i.price) <= j[1]:
                temp_dict[j].append(float(i.qty))
                break
    for i in temp_dict:
        print(i, sum(temp_dict[i]))

if __name__ == '__main__':
    diff_list = diff_price(max_price=2100.0, min_price=1964.1, keep_rate=0.1)
    # buy_sell_percent(*cal_buy_sell_1st(obj))
    cal_volumn_diff(obj, diff_list)
