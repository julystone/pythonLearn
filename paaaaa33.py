import datetime
import re
import shutil

from lxml import etree
from requests.sessions import Session



url = 'http://news.epolestar.xyz/'

my_session = Session()

start_page = 1
end_page = 1672


def get_csrf():
    temp = my_session.get(url, timeout=5)
    csrf = re.search("csrftoken=(.*) for", str(temp.cookies)).group(1)
    return csrf


data = {"userid": "july", "password": "Es123456", "csrfmiddlewaretoken": get_csrf()}

my_session.post(url, data=data, timeout=5)

line = 2
for feedback_id in range(start_page, end_page):
    start = datetime.datetime.now()
    url_new = url + f'feedback/item/{feedback_id}'
    res = my_session.get(url + f'feedback/item/{feedback_id}', timeout=5)
    if res.status_code != 200: continue
    html = res.text
    html = etree.HTML(html)

    ticketStatus = html.xpath('//html/body//div[@class="modal-content"]/div[1]/h4/text()')
    hardVersion = html.xpath('//html/body//div[@class="modal-body"]/div[1]/div[1]/div[1]/p/text()')
    Android = html.xpath('//html/body//div[@class="modal-body"]/div[1]/div[1]/div[2]/p/text()')
    AppVersion = html.xpath('//html/body//div[@class="modal-body"]/div[1]/div[1]/div[3]/p/text()')

    DeviceFac = html.xpath('//html/body//div[@class="modal-body"]/div[1]/div[2]/div[1]/p/text()')
    MobilePhone = html.xpath('//html/body//div[@class="modal-body"]/div[1]/div[2]/div[3]/p/text()')
    Desc = html.xpath('//html/body//div[@class="modal-body"]/div[2]/p[2]/text()')

    if not html.xpath('//html/body//div[@class="modal-body"]/div[3]'):
        picExist = False
    else:
        picExist = True
    ticketId = re.search("(\d.*\d)", str(ticketStatus)).group(1)
    status = re.search("（(.*)）'", str(ticketStatus)).group(1)

    if 1:
        or_list = [ticketId, status, hardVersion, DeviceFac, Android, AppVersion, url_new, MobilePhone, picExist,
                   Desc]
        op_list = []
        for item in or_list:
            if "'" not in str(item):
                op_list.append(str(item))
                continue
            try:
                op_list.append(re.search("：(.*)'", str(item)).group(1))
            except AttributeError:
                op_list.append(re.search("'(.*)'", str(item)).group(1))

        # f.write(f"{url_new}\t{MobilePhone}\t{AppVersion}\t{Desc}\n")
        for i in range(op_list.__len__()):
            my_excel.w_data_origin(line, i + 1, op_list[i])

        line += 1
        end = datetime.datetime.now()
        print(ticketId, end - start)

my_session.close()
my_excel.close()
my_excel.save()
shutil.copy("./result.xlsx", f"./result_{start_page}-{ticketId}.xlsx")

# #
# 前一位：
# ../div[@="class"]/preceding-sibling::div[1]
# 后一位：
# ../div[@="class"]/following-sibling::div[1]
