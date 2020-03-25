import threading
import time


def worker():
    print("i am a thread")
    t = threading.current_thread()
    time.sleep(100)
    print(t.getName())


new_t = threading.Thread(target=worker, name="sub-thread")
new_t.start()

t = threading.current_thread()
print(t.getName())
