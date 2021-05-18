def aaa():
    a = 1
    b = 'test'
    yield a
    yield b


if __name__ == '__main__':
    g = aaa()
    a = next(g)
    b = g.__next__()

    print(a, b)
