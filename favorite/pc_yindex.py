# encoding: utf-8
from math import ceil, floor, log10


def get_data(filename):
    from Utils.Excelize import ReadExcel
    res = ReadExcel(filename).read_data_obj()
    return res

def if_interval_fits(data_range, step, ideal_intervals_min=5, ideal_intervals_max=7,  special_num=None):
    # 计算此步长下的间隔数
    num_intervals = data_range / step
    flag = False

    # 处理特殊情况
    if special_num:
        if special_num - 1 < num_intervals < special_num:
            print(f"遇见{data_range}特殊间隔数，使用特殊步长 {step} 匹配 {special_num} 个间隔")
            flag = True
    # 如果间隔数在理想范围内，这是一个候选
    elif ideal_intervals_min <= num_intervals <= ideal_intervals_max:
        flag = True

    return flag


def find_optimal_step(data_max, data_min, ideal_intervals_min=5, ideal_intervals_max=7, special_num=None):
    """
    计算最优的坐标刻度步长，返回步长、最大值对应的刻度数、最小值对应的刻度数
    :param data_max: 数据的最大值
    :param data_min: 数据的最小值
    :param ideal_intervals_min: 理想的坐标刻度数的最小值, 默认为5
    :param ideal_intervals_max: 理想的坐标刻度数的最大值，默认为7
    :param special_num: 有特殊指定要求的坐标刻度数，默认为None
    :return: 最优的坐标刻度步长、最大值对应的刻度数、最小值对应的刻度数
    """
    # 1. 计算数据大致范围
    raw_data_range = data_max - data_min

    # 2. 定义首选的步长候选值 (1-2-5数量级体系)，由raw_data_range确定数量级大小
    base = (1, 2, 3, 5)
    middle = int(log10(raw_data_range / 6))
    exponents = range(middle - 1, middle + 1)
    preferred_steps = list(round(b * 10 ** exp, 2) for exp in exponents for b in base)
    optimal_step = None

    # 3. 尝试使用原始数据范围
    for step in preferred_steps:
        temp = raw_data_range
        res =  if_interval_fits(temp, step, ideal_intervals_min, ideal_intervals_max, special_num)
        if res:
            optimal_step = step
            break

    # 4. 没找到合适的步长，尝试使用扩展因子
    if not optimal_step:
        expansion_factors = [0.1, 0.2, 0.3]
        for factor in expansion_factors:
            # 计算扩展后的数据范围
            adjusted_data_range = raw_data_range * (1 + factor)
            for step in preferred_steps:
                res = if_interval_fits(adjusted_data_range, step, ideal_intervals_min, ideal_intervals_max, special_num)
                if res:
                    optimal_step = step
                    break

            # 找到第一个符合条件的步长，提前退出循环
            if optimal_step:
                break

    # 6. 特殊情况处理：仍然找不到满意的步长uv，则返回1
    if not optimal_step:
        print("找不到合适的步长，使用1作为步长")
        optimal_step = 1

    # 计算最大值对应的刻度数
    max_yindex = round(ceil(data_max / optimal_step) * optimal_step, 1)
    # 计算最小值对应的刻度数
    min_yindex = round(floor(data_min / optimal_step) * optimal_step, 1)

    return optimal_step, max_yindex, min_yindex


def test(filename):
    # 定义理想间隔数范围 (可接受5到7个)
    ideal_num_intervals_min = 5
    ideal_num_intervals_max = 7

    data_sets_raw = get_data(filename)
    data_sets = []
    for obj in data_sets_raw:
        data_sets.append((obj.name, obj.max_val, obj.min_val, obj.step, obj.special_num))  # 此处name等未定义属性名，为Excel中自带的名称

    # 为每个数据集计算最优步长并与预期比较
    from prettytable import PrettyTable
    table = PrettyTable(
        ["品种名称", "数据最大值", "数据最小值", "坐标最大值", "坐标最小值", "预期步长", "计算步长", "是否匹配"])

    mismatches = 0
    for i, (name, max_val, min_val, expected, special_num) in enumerate(data_sets):
        optimal_step, max_yindex, min_yindex = find_optimal_step(max_val, min_val, ideal_num_intervals_min,
                                                                 ideal_num_intervals_max, special_num)

        match = "✓" if optimal_step == expected else "✗"
        mismatches += 1 if match == "✗" else 0

        table.add_row([name, max_val, min_val, max_yindex, min_yindex, expected, optimal_step, match])

    matches = len(data_sets) - mismatches
    print(table)
    print(f"\n步长完全匹配率: {100 * matches / len(data_sets):.2f}% ({matches}/{len(data_sets)})")


if __name__ == "__main__":
    Excel_file = "../ExcelFiles/step_data.xlsx"
    test(Excel_file)
