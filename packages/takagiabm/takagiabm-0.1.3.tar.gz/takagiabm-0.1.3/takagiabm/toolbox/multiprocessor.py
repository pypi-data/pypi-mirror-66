import os
import threading
import multiprocessing

# Main
print('Main:', os.getpid())

# worker function
def worker(sign, lock):
    lock.acquire()
    print(sign, os.getpid())
    lock.release()


# Multi-thread
record = []
lock = threading.Lock()

# Multi-process
record = []
lock = multiprocessing.Lock()

if __name__ == '__main__':
    for i in range(5):
        thread = threading.Thread(target=worker, args=('thread', lock))
        thread.start()
        record.append(thread)

    for thread in record:
        thread.join()
    
    for i in range(5):
        process = multiprocessing.Process(target=worker, args=('process', lock))
        process.start()
        record.append(process)
    
    for process in record:
        process.join()
