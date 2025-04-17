# encoding: utf-8
import datetime
from calendar import calendar

from Utils.Excelize import ReadExcel
import re
from pc_keymapping import mapping_handler
from pc_g_calendar import GLOBAL_DICT, init_data_class
from pc_calendar_zce import get_old_content

CONTRACT_STRING = r'([a-z]{1,2})([0-9]{3,4})'


class CalendarShfe:

    def __init__(self, date):
        self.date = date
        self.listings = {}
        self.expired = {}
        self.posLimit = {}
        self.bond = {}
        self.fee = {}

    def __repr__(self):
        return f"\n In __repr__：\n{repr(self.__dict__)}"


def get_calendar_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return data


def handle_calendar_data(data):
    # bond_pattern = re.compile(r'(.*)(合约保证金率调整为\d.*%。)'|r'合约退出单向大边保证金优惠：\n\n(.*)合约')
    for item in data:
        date_pattern = re.compile(r'\d{8}')
        date = re.findall(date_pattern, item)[0]
        container = init_data_class(date)
        get_listing_data(item, container)
        get_expired_data(item, container)
        # get_posLimit_data(item, container)
        # get_bond_data(item, container)
        # get_fee_data(item, container)

def get_listing_data(item, container):
    content = get_old_content(container, "listings")
    contract_pattern = re.compile(CONTRACT_STRING)
    listing_pattern = re.compile(r'挂牌')
    res_contract = re.findall(contract_pattern, item)
    listing_flag = re.findall(listing_pattern, item)

    if not listing_flag:
        return

    word = f"挂牌"
    content += mapping_handler(res_contract[0][0].upper()) + "|" + res_contract[0][1] + f",{word};\n"
    container.listings.update({"content": content})


def get_expired_data(item, container):
    content = get_old_content(container, "expired")
    contract_pattern = re.compile(CONTRACT_STRING)
    expired_pattern = re.compile(r'最后交易日')
    res_contract = re.findall(contract_pattern, item)
    expired_flag = re.findall(expired_pattern, item)

    if not expired_flag:
        return

    word = f"最后交易日"
    content += mapping_handler(res_contract[0][0].upper()) + "|" + res_contract[0][1] + f",{word};\n"
    container.expired.update({"content": content})


def get_posLimit_data(item, container):
    if not item.限仓提示:
        return
    posLimit_pattern = re.compile(r"从今日起，.*", re.DOTALL)
    posLimit_pattern_contract = re.compile(CONTRACT_STRING + r"(.*?)；")
    res = re.search(posLimit_pattern, item.限仓提示)
    content = get_old_content(container, "posLimit")

    if res:
        new_word = res.group(0)
        res_contract = re.findall(posLimit_pattern_contract, new_word)

        if res_contract:
            for i in res_contract:
                content += mapping_handler(i[0]) + "|" + i[1] + "," + i[2] + ";\n"
    container.posLimit.update({"content": content})


def get_bond_data(item, container):
    content = get_old_content(container, "bond")
    contract_pattern = re.compile(CONTRACT_STRING)
    spec_buy_pattern = re.compile(r'投机买.*?(\d.*?)%；')
    spec_sell_pattern = re.compile(r'投机卖.*?(\d.*?)%；')
    hedge_buy_pattern = re.compile(r'保值买.*?(\d.*?)%；')
    hedge_sell_pattern = re.compile(r'保值卖.*?(\d.*?)%；')
    res_contract = re.findall(contract_pattern, item)
    spec_buy = re.findall(spec_buy_pattern, item)
    spec_sell = re.findall(spec_sell_pattern, item)
    hedge_buy = re.findall(hedge_buy_pattern, item)
    hedge_sell = re.findall(hedge_sell_pattern, item)
    # print(res_contract, spec_buy, spec_sell, hedge_buy, hedge_sell)

    if not spec_buy and not spec_sell and not hedge_buy and not hedge_sell:
        return

    word = f"投机/保值买卖保证金均为{spec_buy[0]}%"
    if spec_buy == spec_sell != hedge_buy == hedge_sell:
        word = f"投机/保值买卖保证金分别为{spec_buy[0]}%和{hedge_buy[0]}%"
    content += mapping_handler(res_contract[0][0].upper()) + "|" + res_contract[0][1] + f",{word};\n"
    container.bond.update({"content": content})




def get_fee_data(item, container):
    fee_pattern = re.compile(r"合约交易手续费调整：.*收取", re.DOTALL)
    res = re.search(fee_pattern, item.提示)
    fee_inner_pattern_1 = re.compile(CONTRACT_STRING + r"(.*交易手续费按成交金额的.*‰收取)")
    fee_inner_pattern_2 = re.compile(CONTRACT_STRING + r"(.*交易手续费按.*元/手收取)")

    if res:
        new_word = res.group(0)
        content = ""

        res_contract = re.findall(fee_inner_pattern_1, new_word)
        if res_contract:
            for i in res_contract:
                content += mapping_handler(i[0]) + "|" + i[1] + "," + i[2] + ";\n"

        res_contract2 = re.findall(fee_inner_pattern_2, new_word)
        if res_contract2:
            for i in res_contract:
                content += mapping_handler(i[0]) + "|" + i[1] + "," + i[2] + ";\n"
        container.fee.update({"content": content})


def app():
    Excel_file = '../ExcelFiles/calendar_data/dce_calendar.txt'
    res = get_calendar_data(Excel_file)
    handle_calendar_data(res)


if __name__ == '__main__':
    app()
