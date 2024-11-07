import math

C = [6906, 6820, 6872, 6832, 6856, 6912, 7028, 6938, 7032, 6900, 6802, 6724, 6850, 6918, 6884, 6852, 6842, 6876, 6964,
     6900, 6832, 7064, 7336, 7176, 7316, 7334]


def SQRT(num):
    return math.sqrt(num)


def SQUARE(num):
    return math.pow(num, 2)


def MA(C, N):
    temp = 0
    for i in range(N):
        temp += C[i]
    return temp / N


def STD(C: list, M):
    ma = MA(C, M)
    temp = 0
    for i in range(M):
        temp += SQUARE(C[i] - ma)
    return SQRT(temp / (M - 1))


def TOP(N, M, P):
    mid = MA(C, N)
    tep2 = STD(C, M)
    return mid + P * tep2


if __name__ == '__main__':
    print(MA(C, 26))
    print(STD(C, 26))
    print(TOP(26, 26, 2))
