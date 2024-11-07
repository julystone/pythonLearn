import multiprocessing
import socket
import threading
import time


class MySocket:
    host = socket.gethostname()
    port = 12345
    conn = (host, port)
    temp_list = []

    def server(self):
        producer = socket.socket()
        producer.bind(self.conn)
        print("等待连接")
        producer.listen(5)  # 最大支持5个socket连接
        while True:
            con, addr = producer.accept()  # c是新的socket
            out = str(con.recv(1024), encoding='utf-8')
            self.temp_list.append(out)
            con.close()

    def client_send_socket(self, context):
        consumer = socket.socket()
        consumer.connect(self.conn)
        consumer.send(bytes(str(context), encoding="utf-8"))
        consumer.close()


if __name__ == '__main__':
    sk = MySocket()
    server1 = threading.Thread(target=sk.server, args=())
    server1.start()
    time.sleep(3)
    client1 = multiprocessing.Process(target=sk.client_send_socket, args=(123,))
    client1.start()
    client2 = multiprocessing.Process(target=sk.client_send_socket, args=(456,))
    client2.start()
    client3 = multiprocessing.Process(target=sk.client_send_socket, args=(789,))
    client3.start()
    time.sleep(2)
    print(sk.temp_list)
    server1.join()
