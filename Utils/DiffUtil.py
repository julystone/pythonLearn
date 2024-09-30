import json
from collections import deque


def deep_diff(dict1, dict2):
    if dict1 == dict2:
        print("no difference")
        return
    if type(dict1) is not dict or type(dict2) is not dict:
        yield [], dict1, dict2
        return

    queue = deque([([], dict1, dict2)])
    while True:
        new_queue = deque()
        for path, d1, d2 in queue:
            keys1 = set(d1.keys())
            keys2 = set(d2.keys())
            for key in keys1.union(keys2):
                val1 = d1.get(key, None)
                val2 = d2.get(key, None)
                if val1 != val2:
                    if type(val1) is dict and type(val2) is dict:
                        new_queue.append((path + [key], val1, val2))
                    else:
                        yield path + [key], val1, val2

        queue = new_queue
        if not queue:
            break


if __name__ == '__main__':
    with open("../tempFiles/0926135634_ESTEST015_iOS_Setting.json", 'r') as f1:
        json1 = json.load(f1)
    with open("../tempFiles/0926142702_ESTEST015_And_Setting.json", 'r') as f2:
        json2 = json.load(f2)

    res = deep_diff(json1, json2)
    # res.__next__()
    for path, val1, val2 in deep_diff(json1, json2):
        # for key in path:
        #     print(f"{key}:")
        print(path, val1, val2)
