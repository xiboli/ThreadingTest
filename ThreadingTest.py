import threading
import numpy as np
import time
queue_num = 5
rd_pos = 0
j = 0
full_flg = np.zeros((queue_num, 1))
rdwr_lock = threading.Lock()


def dat():
    wr_pos = 0
    for i in range(7):
            # 1. Waiting
            while True:
                rdwr_lock.acquire()
                if full_flg[wr_pos] == 1:
                    rdwr_lock.release()
                    print("run waiting loop")
                    time.sleep(1)
                    continue
                rdwr_lock.release()
                print("run waiting and break")
                break
            # 2. Reading data
            print("run dat function %d" %i)
            # 3. Update flags
            rdwr_lock.acquire()
            full_flg[wr_pos] = 1
            rdwr_lock.release()
            print("run update flags in dat")
            wr_pos = (wr_pos + 1) % queue_num


wr_thread = threading.Thread(target=dat)
wr_thread.start()

for i in range(100):
        # 1. Read data for each batch
        while True:
            rdwr_lock.acquire()
            if full_flg[rd_pos] == 0:
                rdwr_lock.release()
                print("lock acquire %d times before sleep" % j)
                time.sleep(1)
                print("lock acquire %d times after sleep" %j)
                j = j + 1
                continue
            rdwr_lock.release()
            break
        # 2. Training
        print("main function loop %d times" % i)

        # 3. Update flags
        rdwr_lock.acquire()
        full_flg[rd_pos] = 0
        print("run update flags")
        rdwr_lock.release()
        rd_pos = (rd_pos + 1) % queue_num

        i = i + 1



