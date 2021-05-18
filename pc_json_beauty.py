import json
from datetime import datetime

file = "./json_files/000734.json"
# for i in range(782, 824):
#     if i == 800:
#         continue
#     file = f"./json_files/000{i}.json"

with open(file, mode='r') as f:
    res = json.load(f)
    print(res)

out = json.dumps(res, sort_keys=True, indent=4, ensure_ascii=False).encode('utf-8')
with open(f'{file[:-5]}_{datetime.now().strftime("%H%M%S")}.txt', mode='wb+') as f:
    f.write(out)
