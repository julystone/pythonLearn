import json
import logging
import os.path
import time
from multiprocessing import Queue, Process, Manager

from src.main.run_suite import Alistar, DEBUG
from utils.ConfigUtil import my_config
from utils.RedisUtil import uzi_redis as redis

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %a',
                    filename=os.path.join(os.getcwd(), 'log.txt'))
logger = logging.getLogger(__name__)


class Dispatcher:
    def __init__(self):
        self.dict = Manager().dict()
        self.queue = Queue()
        self.device_list = None

    def consume_data(self, device, dict):
        print("start to consume_data" + str(os.getpid()))
        while True:
            data = self.queue.get()
            logger.info(data)
            v_id = data.get('VersionId', None)
            url = data.get('DownloadUrl', None)
            if not v_id or not url:
                logger.error('数据错误')
                return
            if not DEBUG:
                url = 'http://news.epolestar.xyz' + url
            test_case = my_config.get('debug_mode', 'test_case')
            mark = my_config.get('debug_mode', 'mark')
            print("出问题的pid" + str(os.getpid()))
            Alistar(v_id, url, device, test_case, mark).run()
            print(f'{v_id}finished')

    def receive_data(self, dict):
        print("start to produce_data" + str(os.getpid()))
        pb = redis.subscribe()
        if not pb:
            logger.error("启动失败 缺少redis")

        logging.info("alistar start up")
        for item in pb.listen():
            if not item:
                continue
            # try:
            value_type = item.get('type', '')
            value = item.get('data', None)
            if value_type != 'message' or not value:
                continue
            value = json.loads(value)
            logging.info(f"接收到数据{value}")
            key = value['VersionId']
            if key not in dict.keys():
                dict[key] = False
                self.queue.put(value)
            else:
                print('Task has been in Queue or UnderDoing, Plz Wait for finish')

    def adb_dispatch(self):
        import subprocess
        p = subprocess.Popen("adb devices", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                             shell=True)
        (output, err) = p.communicate()
        import re
        pattern = r"(127.0.0.1:21\d{2}3)\sdevice"
        match = re.compile(pattern).findall(output.decode())
        if not match:
            raise Exception(f"can't get {pattern}")
        self.device_list = match

    def app(self):
        print("app" + str(os.getpid()))
        self.adb_dispatch()
        p1 = Process(target=self.receive_data, args=(self.dict, ))
        p1.start()
        time.sleep(3)
        for device in self.device_list:
            c1 = Process(target=self.consume_data, name=device, args=(device, self.dict))
            c1.start()
            time.sleep(3)
        # self.receive_data()


def debug_msg():
    print("debug_msg" + str(os.getpid()))
    data = {'VersionId': '120',
            'DownloadUrl': 'http://news.epolestar.xyz/flask/version/file/download/?versionId=120&type=2&projectType=A'}
    redis.publish_autotest_msg(data=data)


if __name__ == '__main__':
    main_process = Process(target=Dispatcher().app)
    main_process.start()
    time.sleep(10)
    sub_process = Process(target=debug_msg)
    sub_process.start()
    time.sleep(20)
    sub_process2 = Process(target=debug_msg)
    sub_process2.start()
    time.sleep(30)
    sub_process3 = Process(target=debug_msg)
    sub_process3.start()
    # time.sleep(3)
    # sub_process4 = Process(target=debug_msg)
    # sub_process4.start()
    print("pass")
