import pprint
from findit import FindIt

# findit 是个图像识别库，可以依据icon模版，识别出目标图片中的icon所在位置

fi = FindIt(engine=['template'])

print(fi.engine_list)
fi.load_template("add", pic_path="../pics/add.jpg")

result = fi.find(
    target_pic_name='main',
    target_pic_path='../pics/main3.png'
)

print(result['data']['add']['TemplateEngine']['ok'])
print(result['data']['add']['TemplateEngine']['target_point'])
pprint.pprint(result)