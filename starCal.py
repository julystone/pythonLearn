dic1 = {"青铜": 3, "白银": 4, "黄金": 4, "铂金": 5, "钻石": 5, "星耀": 5}
dic2 = {"青铜": 0, "白银": 9, "黄金": 21, "铂金": 37, "钻石": 62, "星耀": 87, "王者": 112}
dic3 = {"青铜": 6, "白银": 5, "黄金": 4, "铂金": 3, "钻石": 2, "星耀": 1, "王者": 0}
dic4 = {v: k for k, v in dic3.items()}


def anay(text, level, stars):
    if text not in dic2.keys():
        print("Err")
    if "王者" in text:
        return dic2[text] + stars
    elif "白银" in text:
        return dic2[text] + dic1[text] * (dic1[text] - level - 1) + stars
    else:
        return dic2[text] + dic1[text] * (dic1[text] - level) + stars


if __name__ == '__main__':
    text_menu = """
    0. 王者
    1. 星耀
    2. 钻石
    3. 铂金
    4. 黄金
    5. 白银
    6. 青铜
    """
    print(text_menu)
    start_text = dic4.get(int(input("text：")))
    start_level = int(input("level："))
    start_star = int(input("star："))
    print(text_menu)
    end_text = dic4.get(int(input("text：")))
    end_level = int(input("level："))
    end_star = int(input("star："))

    # start_text = '青铜'
    # start_level = 3
    # start_star = 1
    # end_text = '王者'
    # end_level = 2
    # end_star = 10
    res = anay(end_text, end_level, end_star) - anay(start_text, start_level, start_star)
    print(res)
