# encoding: utf-8
from datetime import datetime

from pc_g_calendar import monthly_calendar, GLOBAL_DICT
from pc_calendar_zce import app as zce_app
from pc_calendar_dce import app as dce_app
from pc_calendar_shfe import app as shfe_app
from pc_calendar_cffex import app as cffex_app

import pandas as pd


def date_trim(date_str):
    formatted_date = datetime.strptime(date_str, "%Y%m%d").strftime("%Y/%m/%d")
    return formatted_date

def save_to_excel():
    data = {
        '日期': [date_trim(container.date) for container in GLOBAL_DICT.values()],
        '挂牌': [container.listings.get("content", "") for container in GLOBAL_DICT.values()],
        '到期日': [container.expired.get("content", "") for container in GLOBAL_DICT.values()],
        '限仓': [container.posLimit.get("content", "") for container in GLOBAL_DICT.values()],
        '保证金': [container.bond.get("content", "") for container in GLOBAL_DICT.values()],
        '手续费': [container.fee.get("content", "") for container in GLOBAL_DICT.values()],
    }

    df = pd.DataFrame(data)
    print(df)
    # 使用正则表达式清除所有末尾换行符
    df = df.replace(r'\n+$', '', regex=True, inplace=False)

    df.to_excel('./calendar.xlsx')


def main():
    monthly_calendar()

    zce_app()
    dce_app()
    shfe_app()
    cffex_app()


    save_to_excel()

if __name__ == '__main__':
    main()
