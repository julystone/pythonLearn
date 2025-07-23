from Crypto.Util.number import ceil_div

from Utils.Excelize import ReadExcel
from prettytable import PrettyTable


def get_data(filename):
    res = ReadExcel(filename).read_data_obj()
    return res


def find_optimal_step(data_max, data_min):
    """
    根据数据的原始最小值和最大值，计算量柱图y轴的最优刻度步长。

    参数:
    data_min (float): 数据的原始最小值
    data_max (float): 数据的原始最大值

    返回:
    float: 推荐的最优刻度步长
    """
    # 1. 计算数据的原始范围
    raw_data_range = data_max - data_min

    # 2. 定义首选的步长候选值 (1-2-5数量级体系)
    base = (1, 2, 3, 5)
    exponents = range(-2, 6)

    # 3. 定义首选的步长候选值 从0.01到10000
    preferred_steps = list(round(b*10**exp, 2) for exp in exponents for b in base)

    # 3. 计算理想间隔数范围 (可接受5到7个)
    ideal_num_intervals_min = 5
    ideal_num_intervals_max = 7

    # 4. 尝试使用原始数据范围
    for step in preferred_steps:
        # 如果步长为0，则跳过
        if step == 0:
            continue

        # 计算此步长下的间隔数
        num_intervals = raw_data_range / step

        # 如果间隔数在理想范围内，这是一个候选
        if ideal_num_intervals_min <= num_intervals <= ideal_num_intervals_max:
            return step

    # 5. 如果使用原始数据范围找不到合适的步长，尝试扩大显示范围
    expansion_factors = [1.1, 1.2, 1.3, 1.5, 2.0]
    for factor in expansion_factors:
        adjusted_data_range = raw_data_range * factor

        for step in preferred_steps:
            # 如果步长为0，则跳过
            if step == 0:
                continue

            # 计算此步长下的间隔数
            num_intervals = adjusted_data_range / step

            # 如果间隔数在理想范围内，这是一个候选
            if ideal_num_intervals_min <= num_intervals <= ideal_num_intervals_max:
                return step

    # 6. 特殊情况处理：如果仍然找不到满意的步长
    return 1


# 示例使用
if __name__ == "__main__":
    # 测试数据
    Excel_file = "./ExcelFiles/step_data.xlsx"
    data_sets_raw = get_data(Excel_file)
    data_sets = []
    for obj in data_sets_raw:
        data_sets.append((obj.name, obj.max_val, obj.min_val, obj.step))

    # 为每个数据集计算最优步长并与预期比较
    mismatches = 0
    table = PrettyTable(["品种名称", "数据最大值", "数据最小值", "坐标最大值", "坐标最小值", "预期步长", "计算步长", "是否匹配"])
    for i, (name, max_val, min_val, expected) in enumerate(data_sets):
        optimal_step = find_optimal_step(max_val, min_val)

        match = "✓" if optimal_step == expected else "✗"
        mismatches += 1 if match == "✗" else 0
        # 计算最大值对应的刻度数
        from math import ceil, floor
        max_yindex = round(ceil(max_val/optimal_step) * optimal_step, 1)
        # 计算最小值对应的刻度数
        min_yindex = round(floor(min_val / optimal_step) * optimal_step, 1)
        # 计算刻度数差值

        table.add_row([name, max_val, min_val, max_yindex, min_yindex, expected, optimal_step, match])

    # table.min_table_width = 100
    # table.border = False

    print(table)

    print(
        f"\n步长完全匹配率: {100 * (len(data_sets) - mismatches) / len(data_sets):.2f}% ({len(data_sets) - mismatches}/{len(data_sets)})")
