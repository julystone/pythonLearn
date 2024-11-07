#  _____            ___             ____     __
# /\___ \          /\_ \           /\  _`\  /\ \__
# \/__/\ \   __  __\//\ \    __  __\ \,\L\_\\ \ ,_\    ___     ___       __
#    _\ \ \ /\ \/\ \ \ \ \  /\ \/\ \\/_\__ \ \ \ \/   / __`\ /' _ `\   /'__`\
#   /\ \_\ \\ \ \_\ \ \_\ \_\ \ \_\ \ /\ \L\ \\ \ \_ /\ \L\ \/\ \/\ \ /\  __/
#   \ \____/ \ \____/ /\____\\/`____ \\ `\____\\ \__\\ \____/\ \_\ \_\\ \____\
#    \/___/   \/___/  \/____/ `/___/> \\/_____/ \/__/ \/___/  \/_/\/_/ \/____/
#                                /\___/
#                                \/__/
# encoding: utf-8

import timeit

from anyio import sleep


def time_it(func, *args, **kwargs):
    """
    This function is used to time the execution of a function.
    :param func: The function to be timed.
    :param args: The arguments to be passed to the function.
    :param kwargs: The keyword arguments to be passed to the function.
    :return: The time taken to execute the function.
    """
    start_time = timeit.default_timer()
    func(*args, **kwargs)
    end_time = timeit.default_timer()
    return end_time - start_time

if __name__ == '__main__':
    def test_func(n):
        for i in range(n):
            ...

    def test_func_2(n):
        for i in range(n):
            pass

    print(time_it(test_func, 100000))
    print(time_it(test_func_2, 100000))