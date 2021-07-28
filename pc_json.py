import json


with open("./json_files/json_file.txt", mode='r', encoding='utf-8') as f:
    res = json.load(f)


print(res)