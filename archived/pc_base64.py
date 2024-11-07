import base64

from icecream import ic


def base64_encode(image_path):
    with open(image_path, 'rb') as f:
        image = f.read()
    image_base64 = str(base64.b64encode(image), encoding='utf-8')
    return ic(image_base64)


if __name__ == '__main__':
    image_path = r'../pics/add.jpg'
    base64_encode(image_path)
