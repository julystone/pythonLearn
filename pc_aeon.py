# encoding:utf-8


def add_element_to_list(lst, element):
    lst.append(element)
    return lst

def count_successful_pairs(blessings : list):
    """
    计算满足条件的成功命途祝福对数量。

    参数:
        blessings (list): 包含9个命途祝福的列表。

    返回:
        int: 成功命途祝福对的数量。
    """
    count = 0
    for i in range(len(blessings) - 1):  # 遍历到倒数第二个元素
        current = int(blessings[i])  # 假设祝福可以用整数表示（如赋值1-9）
        next_one = int(blessings[i + 1])  # 下一个祝福
        if current + next_one > 6 and current > next_one:
            print(current, next_one)
            count += 1
    print(f"成功命途祝福对的数量为: {count}")


# 示例使用
blessings = ['存护', '记忆', '巡猎', '繁育', '虚无', '智识', '欢愉', '丰饶', '毁灭']
# 注意：在实际应用中，您可能需要将这些字符串映射到整数（例如，通过字典或列表索引）
# 这里为了简化，我假设它们已经是1-9的整数，但实际上您需要替换为相应的整数值

# 假设的整数映射（仅用于示例）
# '存护': 1, '记忆': 2, ... 以此类推

# 由于示例中提供了字符串，我们需要一个映射来将其转换为整数
blessing_map = {
    '存护': 1, '记忆': 2, '巡猎': 3, '繁育': 4,
    '虚无': 5, '智识': 6, '欢愉': 7, '丰饶': 8,
    '毁灭': 9
}

# input_dic =

# 将字符串列表转换为整数列表
# blessings_temp = add_element_to_list(blessings, "存护")
# integer_blessings = [blessing_map[blessings] for blessings in blessings_temp]
#
# 调用函数并打印结果
# success_count = count_successful_pairs(integer_blessings)
# print(f"成功命途祝福对的数量为: {success_count}")