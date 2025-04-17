# encoding: utf-8
import datetime
from Utils.Excelize import ReadExcel
import re

from pc_keymapping import mapping_handler
from pc_g_calendar import init_data_class, GLOBAL_DICT
from pc_calendar_zce import get_old_content

CONTRACT_STRING = r'([A-Z]{1,2})([0-9]{3,4})'


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
    res = ReadExcel(filename).read_data_obj()
    return res


def handle_calendar_data(data):
    # bond_pattern = re.compile(r'(.*)(合约保证金率调整为\d.*%。)'|r'合约退出单向大边保证金优惠：\n\n(.*)合约')
    for item in data:
        date = item.日期.strftime('%Y%m%d')
        container = init_data_class(date)
        get_listing_data(item, container)
        get_expired_data(item, container)
        get_posLimit_data(item, container)
        # get_bond_data(item, container)
        # get_fee_data(item, container)  # ZCE手续费数据暂时不用
        # print(container)


def get_listing_data(item, container):
    if not item.合约挂牌:
        return
    listing_pattern = re.compile(r'(.*?)上市')
    res_contract = re.findall(listing_pattern, item.合约挂牌)
    content = get_old_content(container, "listings")
    if res_contract:
        contract = re.compile(CONTRACT_STRING)
        key_list = []
        for i in res_contract:
            j = re.match(contract, i)
            if not j.group(1):
                continue
            if j.group(1) in key_list:
                continue
            else:
                key_list.append(j.group(1))
            content += mapping_handler(j.group(1)) + "|" + j.group(2) + ",挂牌;\n"
    container.listings.update({"content": content})


def get_expired_data(item, container):
    if not item.合约到期:
        return
    expired_pattern_contract = re.compile(r'(.*?)最后交易日')
    content = get_old_content(container, "expired")

    res_contract = re.findall(expired_pattern_contract, item.合约到期)

    if res_contract:
        contract = re.compile(CONTRACT_STRING)
        key_list = []
        for i in res_contract:
            j = re.match(contract, i)
            if not j.group(1):
                continue
            if j.group(1) in key_list:
                continue
            else:
                key_list.append(j.group(1))
            content += mapping_handler(j.group(1)) + "|" + j.group(2) + ",最后交易日;\n"

    container.expired.update({"content": content})


def get_posLimit_data(item, container):
    if not item.限仓提示:
        return
    posLimit_pattern_contract = re.compile(r"今日起，" + CONTRACT_STRING + r"(.*?手)")
    res = re.findall(posLimit_pattern_contract, item.限仓提示)
    content = get_old_content(container, "posLimit")

    if res:
        for i in res:
            content += mapping_handler(i[0]) + "|" + i[1] + "," + i[2] + ";\n"
    container.posLimit.update({"content": content})


def get_bond_data(item, container):
    if not item.保证金:
        return

    handle_list = item.保证金.split('；')
    contract_pattern = re.compile(CONTRACT_STRING)
    bond_pattern = re.compile(r'交易保证金调整为(.*?)%')
    content = get_old_content(container, "bond")

    for word in handle_list:
        bond = re.findall(bond_pattern, word)
        if not bond:
            continue
        contract = re.findall(contract_pattern, word)
        if not contract:
            continue
        for i in contract:
            content += mapping_handler(i[0]) + "|" + i[1] + ",交易保证金调整为" + bond[0] + "%;\n"

    container.bond.update({"content": content})


def get_fee_data(item, container):
    fee_pattern = re.compile(r"合约交易手续费调整：.*收取", re.DOTALL)
    res = re.search(fee_pattern, item.提示)
    fee_inner_pattern_1 = re.compile(CONTRACT_STRING + r"(.*交易手续费按成交金额的.*‰收取)")
    fee_inner_pattern_2 = re.compile(CONTRACT_STRING + r"(.*交易手续费按.*元/手收取)")

    if res:
        new_word = res.group(0)
        content = get_old_content(container, "fee")

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
    Excel_file = '../ExcelFiles/calendar_data/cffex_calendar.xlsx'
    res = get_calendar_data(Excel_file)
    handle_calendar_data(res)


if __name__ == '__main__':
    app()
    print(GLOBAL_DICT)
