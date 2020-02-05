from multiprocessing import Pool,Lock

def f(l):
    l.acquire()
    try:
        print('hello world')
        print('process id:', os.getpid())
    finally:
        l.release()

if __name__ == '__main__':

    lock = Lock()

    with Pool(10) as p:
        print(p.map(f, lock))