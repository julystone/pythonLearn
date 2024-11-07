from multiprocessing import Manager


def first():
    md = Manager().dict()
    md['a'] = ['a']
    if 'a' in md.keys():
        a = md.get('a')
        a.append('b')
        md['a'] = a
    print(md)


def second():
    md = Manager().dict()
    md['a'] = ['a']
    if 'a' in md.keys():
        md['a'].append('b')
    print(md)


if __name__ == '__main__':
    first()
    second()
