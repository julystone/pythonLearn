# encoding: utf-8

def yield_func(n):
    for i in range(n):
        yield i * i
        if i == 2:
            yield "Hello"


import itertools

def generate_orthogonal_combinations(*args):
    """
    生成多个输入参数的正交组合
    :param args: 每个参数的可能取值，输入形式为：参数1取值, 参数2取值, ...
    :return: 所有可能的组合
    """
    # 使用 itertools.product 生成笛卡尔积
    combinations = list(itertools.product(*args))
    return combinations

# 示例输入
param1 = [1, 2, 3]       # 参数1的可能取值
param2 = ['A', 'B']  # 参数2的可能取值
param3 = [True, False] # 参数3的可能取值

# 生成组合
combinations = generate_orthogonal_combinations(param1, param2, param3)

# 打印结果
for idx, combo in enumerate(combinations):
    print(f"组合 {idx + 1}: {combo}")

#
# if __name__ == '__main__':
#     A = [1, 2, 3]
#     B = ['cat', 'dog', 'bird', 'fish']
#     print(list(zip(A, B)))
#
#     print(list(yield_func(5)))
