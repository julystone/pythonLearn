import pc_factory2
import pc_factory1


class A3:
    @staticmethod
    def return1():
        return pc_factory1.A1()

    @staticmethod
    def return2():
        return pc_factory2.A2()
