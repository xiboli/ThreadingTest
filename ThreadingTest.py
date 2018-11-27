import threading
import numpy as np
import time
queue_num = 5
rd_pos = 0
j = 0
full_flg = np.zeros((queue_num, 1))
rdwr_lock = threading.Lock()


def data_read():
    wr_pos = 0
    for i in range(10):
            # 1. Waiting
            while True:
                rdwr_lock.acquire()
                if full_flg[wr_pos] == 1:
                    rdwr_lock.release()
                    print("run main function loop")
                    time.sleep(1)
                    continue
                rdwr_lock.release()
                print("begin to read data")
                break
            # 2. Reading data
            print("read data in %d position" %i)
            # 3. Update flags
            rdwr_lock.acquire()
            full_flg[wr_pos] = 1
            rdwr_lock.release()
            print("run update flags in data_read function")
            wr_pos = (wr_pos + 1) % queue_num


wr_thread = threading.Thread(target=data_read)
wr_thread.start()
print('first threading')
for i in range(100):
        # 1. Read data for each batch
        while True:
            rdwr_lock.acquire()
            if full_flg[rd_pos] == 0:
                rdwr_lock.release()
                print("jump to read_data function %d times" % j)
                time.sleep(1)
                print("jump out read_data function %d times" %j)
                j = j + 1
                continue
            rdwr_lock.release()
            break
        # 2. Training
        print("main function loop %d times" % i)

        # 3. Update flags
        rdwr_lock.acquire()
        full_flg[rd_pos] = 0
        print("run update flags in main function %d times" % i)
        rdwr_lock.release()
        rd_pos = (rd_pos + 1) % queue_num

        i = i + 1



