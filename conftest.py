import pytest


# conftest.py


# TODO 添加失败、成功截图、每次assert进行截图、截图监听器
@pytest.fixture(scope="function")
def PageInit(func, Page):
    print('test started')
    try:
        Page()
    except AttributeError:
        func()
    yield
    try:
        Page()
    except AttributeError:
        pass
    print('test ended')
