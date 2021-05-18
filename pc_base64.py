import base64

image_path = r'C:\Users\Administrator\Pictures\QQ浏览器截图\QQ浏览器截图20201211092221.png'
with open(image_path, 'rb') as f:
    image = f.read()
    image_base64 = str(base64.b64encode(image), encoding='utf-8')


print(image_base64)