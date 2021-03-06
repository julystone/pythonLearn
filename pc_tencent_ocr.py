"""
  印刷文字识别WebAPI接口调用示例接口文档(必看)：https://doc.xfyun.cn/rest_api/%E5%8D%B0%E5%88%B7%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB.html
  上传图片base64编码后进行urlencode要求base64编码和urlencode后大小不超过4M最短边至少15px，最长边最大4096px支持jpg/png/bmp格式
  (Very Important)创建完webapi应用添加合成服务之后一定要设置ip白名单，找到控制台--我的应用--设置ip白名单，如何设置参考：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=41891
  错误码链接：https://www.xfyun.cn/document/error-code (code返回错误码时必看)
  @author iflytek
"""
# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import json

# from urllib import parse
# 印刷文字识别 webapi 接口地址
URL = "https://ocr.tencentcloudapi.com/?Action=GeneralBasicOCR"
# 应用ID (必须为webapi类型应用，并印刷文字识别服务，参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481)
APPID = "5fd1ebcd"
# 接口密钥(webapi类型应用开通印刷文字识别服务后，控制台--我的应用---印刷文字识别---服务的apikey)
API_KEY = "50a66ea0cc6402cdc1637eb30f449926"


def getHeader():
    #  当前时间戳
    curTime = str(int(time.time()))
    #  支持语言类型和是否开启位置定位(默认否)
    param = {"language": "cn|en", "location": "true"}
    param = json.dumps(param)
    paramBase64 = base64.b64encode(param.encode('utf-8'))

    m2 = hashlib.md5()
    str1 = API_KEY + curTime + str(paramBase64, 'utf-8')
    m2.update(str1.encode('utf-8'))
    checkSum = m2.hexdigest()
    # 组装http请求头
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


# 上传文件并进行base64位编码
with open(r'./pics/main.jpg', 'rb') as f:
    f1 = f.read()

f1_base64 = str(base64.b64encode(f1), 'utf-8')

data = {
    'image': f1_base64
}

r = requests.post(URL, data=data, headers=getHeader())
result = str(r.content, 'utf-8')

out = json.dumps(json.loads(result), sort_keys=True, indent=4, ensure_ascii=False)
# 错误码链接：https://www.xfyun.cn/document/error-code (code返回错误码时必看)
print(out)
input("Entry the any key to exit")
