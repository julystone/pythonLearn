pool = ["happy", "sad", "saddness"]

st = "happ"


def find_in_pool(target, pool):
    for word in pool:
        if target in word:
            print('[yes]')
            break
        return word


st2 = '/awe/f1/z/gq'


def level_teller(target):
    res = target.split('/')[1:]
    return res


if __name__ == '__main__':
    print(level_teller(st2))
