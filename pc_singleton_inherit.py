class Singleton:
    _instance = None
    _count = 0

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        print(cls._count)
        return cls._instance


class SingletonInherit(Singleton):
    pass

    class SS(Singleton):
        def __init__(self):
            print("not singleton")


if __name__ == '__main__':
    a = Singleton()
    b = Singleton()
    c = SingletonInherit()
    d = SingletonInherit()
    e = SingletonInherit.SS()
    f = SingletonInherit.SS()
