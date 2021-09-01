import pprint
from findit import FindIt

fi = FindIt(engine=['template'])

# print(fi.engine_list)
fi.load_template("add", pic_path="./pics/add.jpg")

result = fi.find(
    target_pic_name='main',
    target_pic_path='./pics/main3.png'
)

print(result['data']['add']['TemplateEngine']['ok'])
print(result['data']['add']['TemplateEngine']['target_point'])
pprint.pprint(result)