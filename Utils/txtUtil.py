# encoding: utf-8

import re

text_file = './output.txt'
with open(text_file, 'r', encoding='utf-8') as file:
    text = file.read()
print(text)
pattern = "(\D)\d*．(\D)"
res = re.findall(pattern, text)
print(res)

