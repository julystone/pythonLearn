import json
from enum import IntEnum, unique, auto

from Utils.CaptchaUtil import create_captcha
from Utils.HttpUtil import HttpRequestNoCookie


@unique
class SourceType(IntEnum):
    App = auto()
    PC = auto()


@unique
class DataType(IntEnum):
    Self = auto()
    Setting = auto()


@unique
class DeviceType(IntEnum):
    And = auto()
    iOS = auto()
    EsX = auto()


class Synchronize:
    def __init__(self, userNo, source, dataType, device):
        self.userNo = userNo
        self.source = source
        self.dataType = dataType
        self.device = device
        self.captcha, self.time_str = create_captcha()

        # self.data_str = self.ParamDict["dataType"][dataType]
        self.data_str = DataType(dataType).name
        self.device_str = DeviceType(device).name
        self.res = None
        self.out = None
        self.get_res()

    def get_res(self):
        data = {
            "userNo": self.userNo,
            "source": self.source,
            "dataType": self.dataType,
            "captcha": self.captcha
        }

        h = {
            'Connection': "keep-alive",
            'User-Agent': "Mozilla/5.0",
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cookie': "*",
        }

        url = 'https://news.epolestar.xyz/flask/terminal/auth/server/'

        method = 'POST'

        self.res = HttpRequestNoCookie.request(method=method, url=url, json=data, headers=h)

    def common_get(self):
        self.out = json.dumps(json.loads(self.res), sort_keys=True, indent=4, ensure_ascii=False)

    def setting_analyze_get(self):
        if self.dataType == 1:
            self.out = "Param Error：Not setting type"
            return
        # self.out = json.dumps(json.loads(self.res)["Data"]["SettingsConfig"]["EsKLineAnalysisLines"],
        self.out = json.dumps(
            json.loads(self.res).get("Data", {}).get("SettingsConfig", {}).get("EsKLineAnalysisLines", []),
            sort_keys=True,
            indent=4, ensure_ascii=False)

    def setting_without_header(self):
        if self.dataType == 1:
            self.out = "Param Error：Not setting type"
            return
        data = json.loads(self.res).get("Data", {}).get("SettingsConfig", {})
        ok = {}
        for key in data:
            if "Header" in key or "|" in key:
                continue
            ok[key] = data[key]
        self.out = json.dumps(ok, sort_keys=True, indent=4, ensure_ascii=False)

    def write_file(self):
        with open(f'../tempFiles/{self.name_format}', mode='w+') as f:
            f.write(self.out)

    def file_bytes(self):
        return self.out.encode()

    @property
    def name_format(self):
        return f"{self.time_str[4:]}_{self.userNo}_{self.device_str}_{self.data_str}.json"


if __name__ == '__main__':
    userNo = "ESTEST015"
    source = SourceType.App  # 1:App, 2:PC
    dataType = DataType.Setting  # 1:Self,2:Setting

    device = DeviceType.And  # 1:And, 2:iOS, 3:EsX

    out = Synchronize(userNo, source, dataType, device)
    out.common_get()
    out.write_file()
