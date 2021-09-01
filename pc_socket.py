import multiprocessing
import socket
import time


def first():
    s = socket.socket()
    print("this is socket")
    print("等待连接")
    host = socket.gethostname()
    port = 12345
    s.bind((host, port))
    s.listen(5)

    while True:
        c, addr = s.accept()  # c是新的socket
        print(addr)
        sb = bytes("hello to socket,欢迎连接到服务器", encoding="utf-8")
        c.send(sb)
        c.close()


def second():
    s = socket.socket()
    host = socket.gethostname()
    port = 12345

    s.connect((host, port))
    # print(type(s.recv(1024)))
    # 必须支持中文
    print("客户端：让我连到服务器")
    # print(str(s.recv(1024), encoding="utf8"))
    s.close()


if __name__ == '__main__':
    server = multiprocessing.Process(target=first, args=())
    server.start()
    time.sleep(3)
    client = multiprocessing.Process(target=second, args=())
    client.start()
    client1 = multiprocessing.Process(target=second, args=())
    client1.start()
    client2 = multiprocessing.Process(target=second, args=())
    client2.start()
