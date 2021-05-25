import re
from Utils.DataUtil import ReadExcel

with open('./test.txt', 'r', encoding='utf-8') as f:
    res = f.read()
pattern = re.compile(
    r"比\n([\s|\S]*?)(?=对比)")

excel = ReadExcel("./tempFiles/ships3.xlsx", "Sheet1")
reg_result = pattern.findall(str(res))
line_no = 2
for ship in reg_result:
    ship: str
    ship2 = re.split(r"[\t|\n]", ship)
    column_no = 1
    for attr in ship2:
        if "海王星" in attr:
            print(1)
        excel.w_data_origin(line_no, column_no, attr)
        column_no += 1
    line_no += 1
excel.save()
