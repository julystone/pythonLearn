from enum import Enum

#
# class VIP(Enum):
#     UnicodeError = 1
#     Exception = 2

vip = Enum('11', {"True": 1, "Exception": 2})

if __name__ == '__main__':
    print(vip)
    print(vip.Exception.value)
