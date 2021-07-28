list1 = [3, 4, 8, 13]

list2 = ['+', '-', '*', '/']


def cp(list_unchanged, symbol_list):
    for number1 in list_unchanged:
        list1 = list_unchanged[:]
        list1.remove(number1)
        for symbol1 in symbol_list:
            for number2 in list1:
                list2 = list1[:]
                list2.remove(number2)
                result = eval(f"{number1}{symbol1}{number2}")
                for symbol2 in symbol_list:
                    for number3 in list2:
                        list3 = list2[:]
                        list3.remove(number3)
                        result2 = eval(f"{result}{symbol2}{number3}")
                        for symbol3 in symbol_list:
                            for number4 in list3:
                                str1 = f"{number1}{symbol1}{number2}{symbol2}{number3}{symbol3}{number4}"
                                res = eval(f"{result2}{symbol3}{number4}")
                                if res == 24:
                                    print(str1)


def choose_number(ll):
    for i in ll:
        yield i


if __name__ == '__main__':
    list1 = []
    for _ in range(4):
        list1.append(int(input(f"input ur {_+1} number:")))

    cp(list1, list2)
