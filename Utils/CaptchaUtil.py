import random
import string
from datetime import datetime


def create_captcha() -> tuple:
    # 1. 随机生成10位的字符串（包含大小写字母和数字）
    captcha_chars = string.ascii_letters + string.digits  # 包含大小写字母和数字的字符集
    captcha = ''.join(random.choices(captcha_chars, k=10))

    # 2. 获取当前时间并格式化为字符串
    now = datetime.now()
    time_str = now.strftime("%Y%m%d%H%M%S")

    # 3. 计算基于验证码和时间戳的某种值（这里简化为验证码字符的ASCII码之和）
    # 注意：这里不直接使用时间字符串的字符作为索引，因为长度可能不匹配
    sum_value = 0
    for index in time_str:
        sum_value += ord(captcha[ord(index) - ord('0')])
    # sum_value = sum(ord(char) for char in captcha)  # 累加验证码字符的ASCII码
    sum_str = str(sum_value)[-3:].zfill(3)  # 取最后三位，不足则补零

    # 返回完整的验证码字符串
    return captcha + time_str + sum_str, time_str
