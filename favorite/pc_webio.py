from icecream import ic
from pywebio.input import input, radio, input_group
from pywebio.output import put_file, put_code, put_text,put_buttons
from pywebio import start_server

from favorite.pc_synchronize_pa import Synchronize, SourceType, DataType, DeviceType


def syn():
    info = input_group("获取云端同步的json文件", [
        input("行情账号:", required=True, name="userNo"),
        radio("云端同步来源:", options=[("移动端", SourceType.App, True), ("PC", SourceType.PC)], required=True,
              name="source"),
        radio("云端数据类型:", options=[("自选数据", DataType.Self), ("设置数据", DataType.Setting, True)],
              required=True, name="dataType"),
        radio("设备类型:",
              options=[("Android", DeviceType.And, True), ("iOS", DeviceType.iOS), ("EstarX", DeviceType.EsX)],
              required=True, name="device")])
    user_no, source, data_type, device = info["userNo"], info["source"], info   ["dataType"], info["device"]
    out = Synchronize(user_no.upper(), source, data_type, device)
    return out

def common_get(out):
    out.common_get()
    put_file(out.name_format, out.file_bytes(), out.name_format)
    put_code(out.out, language='json')

def setting_analyze_get(out):
    out.setting_analyze_get()
    put_file(out.name_format, out.file_bytes(), out.name_format)
    put_code(out.out, language='json')

def setting_without_header_get(out):
    out.setting_without_header()
    put_file(out.name_format, out.file_bytes(), out.name_format)
    put_code(out.out, language='json')


def main():
    out = syn()
    put_text("欢迎使用云端数据同步工具")
    put_buttons([
        dict(label="获取完整数据", value=lambda: common_get(out), color="success"),
        dict(label="仅获取画线分析列表数据", value=lambda: setting_analyze_get(out), color="info"),
        dict(label="获取排除冗余的设置点数、列表表头以外的设置数据", value=lambda: setting_without_header_get(out), color="warning"),
    ], onclick=lambda x: x())
    ic(out.userNo, SourceType(out.source).name, out.data_str, out.device_str, out.time_str)

if __name__ == '__main__':
    start_server(main, port=8080)
