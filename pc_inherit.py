class A:
    def aaa(self):
        print(123)


class B(A):
    pass


class C(B):
    pass


if __name__ == '__main__':
    c = C()
    c.aaa()