def main(do_A, do_B, **kwargs):
    do_A(kwargs['AAA'])
    do_B(kwargs['BBB'])


def do_AA(AAA):
    print(AAA)


def do_BB(BBB):
    print(BBB)


if __name__ == '__main__':
    main(do_AA, do_BB, AAA=111, BBB=222)
