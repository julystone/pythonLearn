import datetime
import re
import shutil

from lxml import etree
from requests.sessions import Session



url = 'http://47.101.65.61/zentao/'

my_session = Session()

start_page = 1
end_page = 1672


def get_csrf():
    temp = my_session.get(url + 'user-login', timeout=5)
    csrf = re.search("csrftoken=(.*) for", str(temp.cookies)).group(1)
    return csrf


# data = {"userid": "july", "password": "wscxz712718", "csrfmiddlewaretoken": get_csrf()}
data = {"userid": "july", "password": "wscxz712718"}

my_session.post(url, data=data, timeout=5)
line = 2
start = datetime.datetime.now()
url_new = url + f'bug-view-7032'
res = my_session.get(url_new, timeout=5)
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

# #
# 前一位：
# ../div[@="class"]/preceding-sibling::div[1]
# 后一位：
# ../div[@="class"]/following-sibling::div[1]
