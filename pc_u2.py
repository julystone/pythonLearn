import uiautomator2 as u2

driver = u2.connect()

login_userNo = ("resourceId", 'esunny.test:id/et_login_userno')

elem = driver(resourceId=login_userNo[1])
res = elem.get_text()

print(res)
