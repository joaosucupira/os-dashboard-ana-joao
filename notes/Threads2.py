import time
import threading
from concurrent import features 


# Thread and Thread.start

def do_sm():
    # print('slp in 1')
    time.sleep(2)
    # print('done slp')

# do_sm()

t1 = threading.Thread(target=do_sm)
t2 = threading.Thread(target=do_sm)
t3 = threading.Thread(target=do_sm)

def do_sm_no_threads():
    s = time.perf_counter()
    do_sm()
    do_sm()
    f = time.perf_counter()
    return round(f - s, 4)

def do_sm_threads():
    s = time.perf_counter()
    t1.start()
    t2.start()
    f = time.perf_counter()
    
    return round(f - s, 4)

def print_ex_1():
    v1 = do_sm_no_threads()
    v2 = do_sm_threads()
    print(f'Time w no threads: {v1}')
    print(f'Time w no threads: {v2}')

# Thread.join

def do_sm_threads_join():
    s = time.perf_counter()
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    time.sleep(1)
    t2.join()
    time.sleep(1)
    t3.join()
    f = time.perf_counter()
    return round(f - s, 4)

def print_ex_2():
    v1 = do_sm_no_threads()
    # v2 = do_sm_threads()
    v3 = do_sm_threads_join()
    print(f'Time w no threads: {v1}')
    # print(f'Time w threads: {v2}')
    print(f'Time w threads joining: {v3}')

# Threads manual

def sleep_thread(seconds):
    print(f'sleepin {seconds} second(s)...')
    time.sleep(seconds)
    print(f'done sleepin...')

def loop_threads():
    threads = []

    for _ in range(10):
        ti = threading.Thread(target=sleep_thread, args=[1.5])
        ti.start()
        threads.append(ti)

    for thread in threads:
        thread.join()

def contar():
    s = time.perf_counter()

    loop_threads()

    f = time.perf_counter()
    return round(f - s, 4)

print(f'Total time = {contar()} seconds')

# Threads easier


