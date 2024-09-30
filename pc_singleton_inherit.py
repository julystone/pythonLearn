# coding: utf-8

from Utils.DataUtil import ReadExcel
import json


def app():
    file_name = "./SearchWords/敏感词语.xlsx"

    OBJ = ReadExcel(file_name)

    all_words = []
    index = 1

    for item in OBJ.read_data_obj():
        result = deal(item.words)
        print(result[0])
        all_words.extend(result[0])
        index += 1
        OBJ.w_data_origin(index, 2, result[1])

    print(all_words)
    with open("./sensitive.json", 'w', encoding='utf-8') as f:
        json.dump(all_words, f, ensure_ascii=False)
    OBJ.save()


def deal(string: str):
    piece_list = string.split("、")
    return piece_list, len(piece_list)


if __name__ == '__main__':
    app()
