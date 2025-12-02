# encoding: utf-8
import re

from DrissionPage import SessionPage

if __name__ == '__main__':
    url = 'https://mp.weixin.qq.com/s/7Yb6NE_d1kRe4R6-HeJG3Q'
    page = SessionPage()
    page.get(url)
    title = page('tag:h1').text
    author = page('@id=js_name').text
    pattern = re.compile(r"var createTime\s*=\s*'([^']*)';")
    match = pattern.search(page.html)
    create_time = "temp"

    if match:
        create_time = match.group(1)
        print("提取到的 createTime：", create_time)
    else:
        print("未找到 createTime 变量")
    time = page('@id=publish_time').raw_text
    print(title)
    print(author)
    print(time)
    print(create_time)
