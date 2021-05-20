import os

import pytest


class Page:
    def __init__(self):
        print("I am a page")


def func():
    print('july')


@pytest.fixture(scope="function")
def PageInit(request):
    print('test started')
    # try:
    #     request.param['func']()
    # except AttributeError:
    #     request.param['func']()q
    # yield
    # try:
    #     request.param['Page']()
    # except AttributeError:
    #     pass
    assert 1 == 1
    print(request)
    print('test ended')


# PageData = [{'func': func, 'Page': Page}, {'func': func, 'Page': Page}]
PageData = {'func': func, 'Page': Page}


# PageData = [func, Page]


@pytest.mark.parametrize('PageInit', PageData, indirect=True)
def testcase_class(PageInit):
    print('do some thing')


if __name__ == '__main__':
    os.system(f"pytest Testcase.py -vsx --lf")
q