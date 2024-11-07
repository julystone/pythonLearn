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


def SMA(X, N, M):
    X = X[:-1]
    if N <= 0:
        return 0
    return (M * X[0] + (N - M) * SMA(X, N - 1, M)) / N


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


def MAX(a, b):
    return b if a < b else a


def ABS(num):
    return abs(num)


def RSI(N1, N2):
    LC = C[1]
    RSI1 = SMA(MAX(C[0] - LC, 0), N1, 1) / SMA(ABS(C[0] - LC), N1, 1) * 100
    RSI2 = SMA(MAX(C[0] - LC, 0), N2, 1) / SMA(ABS(C[0] - LC), N2, 1) * 100
    print(RSI1, RSI2)


if __name__ == '__main__':
    print(MA(C, 26))
    print(STD(C, 26))
    print(TOP(26, 26, 2))
    # RSI(7, 14)
