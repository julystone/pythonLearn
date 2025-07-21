# encoding: utf-8
from math import ceil


def find_optimal_step(data_min, data_max):
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
    preferred_steps = [0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5, 10]

    # 3. 计算理想间隔数范围 (4到6个)
    ideal_num_intervals_min = 4
    ideal_num_intervals_max = 6

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
    return min(preferred_steps)


if __name__ == '__main__':
    # 测试数据
    data_sets = [
        # (最大值, 最小值)
        (1.32, -0.95),  # 国际铜指数
        (1.76, -1.92),  # 白银指数
        (1.02, -1.33),  # 铝指数
        (8.28, -7.42),  # 动力煤
    ]

    # 预期输出
    expected_steps = [0.5, 1, 0.5, 3]

    # 为每个数据集计算最优步长并与预期比较
    mismatches = 0
    print("| 品种       | 最大值 | 最小值 | 计算步长 | 预期步长 | 步长匹配 |")
    print("|------------|--------|--------|----------|----------|----------|")
    for i, (max_val, min_val) in enumerate(data_sets):
        optimal_step = find_optimal_step(max_val, min_val)
        expected = expected_steps[i]

        match = "✓" if optimal_step == expected else "✗"
        mismatches += 1 if match == "✗" else 0

        print(
            f"| {['国际铜指数', '白银指数', '铝指数', '动力煤'][i]} | {max_val:.2f} | {min_val:.2f} | {optimal_step:.1f} | {expected:.1f} | {match} |")
    print(
        f"\n步长完全匹配率: {100 * (len(data_sets) - mismatches) / len(data_sets):.2f}% ({len(data_sets) - mismatches}/{len(data_sets)}")
