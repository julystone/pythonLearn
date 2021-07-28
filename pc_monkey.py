import os

# import uiautomator2 as u2
#
# d = u2.connect('ef14c21f')
# print(d)
# d.app_start(package_name='esunny.estarandroid', use_monkey=True)
#
# print(d.app_current())

packageName = 'esunny.estarandroid'
# activityName = 'com.esunny.ui.common.setting.stopLossOpen.EsStopLossOpenActivity'
serial = 'ef14c21f'
throttle = 50
log_level = 0
cmd_str = f'adb -s {serial} shell monkey ' \
          f'-p {packageName} ' \
          f'--throttle {throttle} ' \
          f'--pct-touch 50 ' \
          f'--pct-pinchzoom 20 ' \
          f'--pct-motion 0 ' \
          f'--pct-trackball 0 ' \
          f'--pct-syskeys 0 ' \
          f'--pct-nav 0 ' \
          f'--pct-majornav 20 ' \
          f'--pct-appswitch 10 ' \
          f'--pct-flip 0 ' \
          f'--pct-anyevent 0 ' \
          f'1000'
# os.system(f"adb shell input swipe {params[0]} {params[1]} {params[2]} {params[3]} {duration}")
for _ in range(5):
    output = os.system(cmd_str)
