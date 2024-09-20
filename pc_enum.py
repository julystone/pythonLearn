from enum import Enum

#
# class VIP(Enum):
#     UnicodeError = 1
#     Exception = 2

vip = Enum(value="Color", names={"True": 1, "Exception": 2})

if __name__ == '__main__':
    print(vip)
    print(vip.Exception.value)
