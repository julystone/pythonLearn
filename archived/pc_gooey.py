from gooey import Gooey, GooeyParser


class MyGooey:
    settings_msg = 'MQTT device activation information subscription'
    parser = GooeyParser(description=settings_msg)

    @Gooey(
        optional_cols=4,
        program_name="pyw_name".capitalize(),
        sidebar_title='功能',
        terminal_font_family='Consolas',
        language='chinese',
        default_size=(800, 850),
        navigation='SIDEBAR',
        tabbed_groups=True,
        show_success_modal=False,
        show_failure_modal=False,
        # show_stop_warning=False,
        # load_build_config='gooey_config.json',
        # dump_build_config='gooey_config.json',
        richtext_controls=False, auto_start=False,
        menu=[{
            'name': '文件',
            'items': [{
                'type': 'AboutDialog',
                'menuTitle': '关于',
                'name': 'AzurLaneAutoScript',
                'description': 'Alas, 一个带GUI的碧蓝航线脚本 (支持国服, 国际服, 日服, 可以支持其他服务器).',
                'website': 'https://github.com/LmeSzinc/AzurLaneAutoScript'
            }, {
                'type': 'Link',
                'menuTitle': '访问Github仓库',
                'url': 'https://github.com/LmeSzinc/AzurLaneAutoScript'
            }]
        }, {
            'name': '帮助',
            'items': [{
                'type': 'Link',
                'menuTitle': 'Wiki',
                'url': 'https://github.com/LmeSzinc/AzurLaneAutoScript/wiki'
            }, {
                'type': 'Link',
                'menuTitle': 'Github Token',
                'url': 'https://github.com/settings/tokens'
            }]
        }]
    )
    def main(self):
        pass

    def addSideBar(self, name):
        return self.parser.add_subparsers(name=name)

    @staticmethod
    def addArgumentLv1(ob, default, choices, he):
        return ob.add_argument_group('关卡设置', '需要运行一次来保存选项', gooey_options={'label_color': '#931D03'})

    @staticmethod
    def addArgumentLv2(ob, default, choices, he):
        return ob.add_argument(default=default, choices=choices, help=he)

def main():
    # parser = GooeyParser(description="My Cool GUI Program!")
    # parser.add_argument('Filename', widget="FileChooser")  # 文件选择框
    # parser.add_argument('Date', widget="DateChooser")  # 日期选择框
    # args = parser.parse_args()  # 接收界面传递的参数
    # print(args)

    settings_msg = 'MQTT device activation information subscription'
    parser = GooeyParser(description=settings_msg)

    subs = parser.add_subparsers(help='commands', dest='command')

    my_cool_parser = subs.add_parser('MQTT消息订阅')
    my_cool_parser.add_argument("connect", metavar='运行环境', help="请选择开发环境", choices=['dev环境', 'staging环境'],
                                default='dev环境')
    my_cool_parser.add_argument("device_type", metavar='设备类型', help="请选择设备类型", choices=['H1', 'H3'])
    my_cool_parser.add_argument("serialNumber", metavar='设备SN号', default='LKVC19060047', help='多个请用逗号或空格隔开')

    siege_parser = subs.add_parser('进度条控制')
    siege_parser.add_argument('num', help='请输入数字', default=100)

    args = parser.parse_args()
    print(args, flush=True)  # 坑点：flush=True在打包的时候会用到

#
# if __name__ == '__main__':
#     main()
