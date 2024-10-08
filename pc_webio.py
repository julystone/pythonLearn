from math import trunc

from pywebio.input import input, FLOAT, radio, input_group
from pywebio.output import put_text, put_file, put_code, put_collapse
from pywebio import start_server

from pc_synchronize_pa import Synchronize


def syn():
    info = input_group("Sync Info", [
        input("User No:", required=True, name="userNo"),
        radio("来源:", options=[("App", 1, True), ("PC", 2)], required=True, name="source"),
        radio("云端数据类型:", options=[("Self", 1), ("Setting", 2, True)], required=True, name="dataType"),
        radio("设备名:", options=[("And", 1, True), ("iOS", 2), ("EstarX", 3)], required=True, name="device")])
    user_no, source, data_type, device = info["userNo"], info["source"], info["dataType"], info["device"]
    out = Synchronize(user_no.upper(), source, data_type, device)
    out.common_get()
    put_file(out.name_format, out.file_bytes(), out.name_format)
    # put_code(out.res, language='json')


def bmi():
    height = input("Your Height(cm)：", type=FLOAT)
    weight = input("Your Weight(kg)：", type=FLOAT)

    BMI = weight / (height / 100) ** 2

    top_status = [(14.9, 'Severely underweight'), (18.4, 'Underweight'),
                  (22.9, 'Normal'), (27.5, 'Overweight'),
                  (40.0, 'Moderately obese'), (float('inf'), 'Severely obese')]

    for top, status in top_status:
        if BMI <= top:
            put_text('Your BMI: %.1f, category: %s' % (BMI, status))
            break


if __name__ == '__main__':
    start_server(syn, port=8080)
