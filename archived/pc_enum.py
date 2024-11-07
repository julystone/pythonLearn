# encoding: utf-8

from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


# 枚举类型的比较
if Color.RED != Color.GREEN:
    print("RED is not the same as GREEN")

print(Color.RED.value)
print(Color.GREEN.name)

num = 1
print(Color(num).name)
# 枚举类型可以作为字典的键值
color_dict = {Color.RED: "红色", Color.GREEN: "绿色", Color.BLUE: "蓝色"}
print(color_dict[Color.RED])     # 红色
