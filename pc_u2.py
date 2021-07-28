import uiautomator2 as u2

driver = u2.connect()

res = driver(text='编队')
print(res)
