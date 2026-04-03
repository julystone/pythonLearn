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
        date = item.时间
        container = init_data_class(date)
        get_listing_data(item, container)
        get_expired_data(item, container)
        get_posLimit_data(item, container)
        get_bond_data(item, container)
        get_fee_data(item, container)
        print(container)


def get_listing_data(item, container):
    listing_pattern = re.compile(r'新合约上市：(.*)合约上市')
    res_contract = re.findall(listing_pattern, item.提示)
    content = get_old_content(container, "listings")

    if res_contract:
        res_list = res_contract[0].split('、')
        print(res_list)
        contract = re.compile(CONTRACT_STRING)
        for i in res_list:
            j = re.match(contract, i)
            if not j.group(1):
                continue
            content += mapping_handler(j.group(1)) + "|" + j.group(2) + ",挂牌;\n"
    container.listings.update({"content": content})


def get_expired_data(item, container):
    expired_pattern_contract = re.compile(r'合约最后交易日：(.*?)合约')
    expired_pattern_option = re.compile(r'期权最后交易日：(.*?)系列')

    res_contract = re.findall(expired_pattern_contract, item.提示)
    res_option = re.findall(expired_pattern_option, item.提示)
    content = get_old_content(container, "expired")

    if res_contract:
        res_list = res_contract[0].split('、')
        contract = re.compile(CONTRACT_STRING)
        for i in res_list:
            j = re.match(contract, i)
            if not j.group(1):
                continue
            content += mapping_handler(j.group(1)) + "|" + j.group(2) + ",最后交易日;\n"

    if res_option:
        res_list = res_option[0].split('、')
        contract = re.compile(CONTRACT_STRING)
        for i in res_list:
            j = re.match(contract, i)
            if not j.group(1):
                continue
            content += mapping_handler(j.group(1), True) + "|" + j.group(2) + ",最后交易日;\n"
    container.expired.update({"content": content})


def get_posLimit_data(item, container):
    posLimit_pattern = re.compile(r"合约限仓：.*?。", re.DOTALL)
    posLimit_pattern_contract = re.compile(CONTRACT_STRING + r"(非期货公司会员的持仓限额为.*手，客户的持仓限额为.*手)")
    posLimit_pattern_option = re.compile(
        CONTRACT_STRING + r"(系列期权非期货公司会员的持仓限额为.*手，客户的持仓限额为.*手)")
    res = re.search(posLimit_pattern, item.提示)
    content = get_old_content(container, "posLimit")

    if res:
        new_word = res.group(0)
        res_contract = re.findall(posLimit_pattern_contract, new_word)
        res_option = re.findall(posLimit_pattern_option, new_word)

        if res_contract:
            for i in res_contract:
                content += mapping_handler(i[0]) + "|" + i[1] + "," + i[2] + ";\n"
        if res_option:
            for i in res_option:
                content += mapping_handler(i[0], True) + "|" + i[1] + "," + i[2] + ";\n"
    container.posLimit.update({"content": content})


def get_bond_data(item, container):
    bond_1_pattern = re.compile(r"合约保证金率调整：.*", re.DOTALL)
    bond_2_pattern = re.compile(r"合约退出单向大边保证金优惠：(.*)合约双边收取保证金", re.DOTALL)
    bond_inner_pattern_1 = re.compile(CONTRACT_STRING + r"合约(保证金率调整为\d*%)")
    res_1 = re.search(bond_1_pattern, item.提示)
    res_2 = re.search(bond_2_pattern, item.提示)
    content = get_old_content(container, "bond")

    if res_1:
        new_word = res_1.group(0)
        res_contract = re.findall(bond_inner_pattern_1, new_word)
        if res_contract:
            for i in res_contract:
                content += mapping_handler(i[0]) + "|" + i[1] + "," + i[2] + ";\n"

    if res_2:
        res_list = res_2[1].split('、')
        contract = re.compile(CONTRACT_STRING)
        for i in res_list:
            j = re.match(contract, i)
            if not j.group(1):
                continue
            content += mapping_handler(j.group(1), True) + "|" + j.group(2) + ",退出单向大边保证金优惠;\n"
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
    Excel_file = ['../ExcelFiles/calendar_data/shfe_calendar.xlsx', '../ExcelFiles/calendar_data/ine_calendar.xlsx']
    for i in Excel_file:
        res = get_calendar_data(i)
        handle_calendar_data(res)


if __name__ == '__main__':
    app()
