import pc_factory3


class A1:
    def __init__(self):
        self.sec = 1

    def b2(self):
        print(self.sec)
        return pc_factory3.A3().return2()


if __name__ == '__main__':
    print(A1().b2())
