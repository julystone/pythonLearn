import threading

global_data = threading.local()


def show():
    print(threading.current_thread().getName(), global_data.hh)


def thread_cal():
    global_data.hh = 0
    for _ in range(1000):
        global_data.hh += 1
    show()


threads = []
for i in range(10):
    threads.append(threading.Thread(target=thread_cal))
    threads[i].start()

print(global_data)
print("Main thread: ", global_data.__dict__)  # {}
