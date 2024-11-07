# encoding:utf-8

# 继承关系：C继承B，B继承A，A没有父类。
# python继承的一次练习
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
