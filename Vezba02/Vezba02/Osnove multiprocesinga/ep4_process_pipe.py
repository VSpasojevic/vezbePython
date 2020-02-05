from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])
    conn.send([53, None, 'new'])
    conn.send([53, None, 'message'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    print(parent_conn.recv())
    
    p.join()