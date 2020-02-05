from multiprocessing.managers import BaseManager 
manager = BaseManager(address=('', 50000), authkey=b'abc') 
server.serve_forever() 
server = manager.get_server()