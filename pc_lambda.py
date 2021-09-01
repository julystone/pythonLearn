aaa = lambda: bb()


class bb:
    def __init__(self):
        self.laughter = "哈哈哈哈"

    def laugh(self):
        print(self.laughter)


def cc(aaa):
    return aaa()


if __name__ == '__main__':
    cc(aaa).laugh()
