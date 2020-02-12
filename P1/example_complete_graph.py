import sys
from multiprocessing import Process, Queue
from msg_passing_api import *


class Mess:
    def __init__(self,type,message,src_port,dest_port):
        self.type = type
        self.message = message
        self.src = src_port
        self.dest = list()
    
class Node:
    def __init__(self,parent,other,children,message):
        self.parent = parent
        self.message = message
        self.children = list()
        self.other = list()

def main():
    # Parse command line arguments
    if len(sys.argv) != 3:
        print('Program usage: example_complete_graph proc_index number_of_proc')
        print('Example: If number_of_proc = 3, we must start 3 instances of program in 3 terminals:')
        print('example_complete_graph 0 3, example_complete_graph 1 3, and example_complete_graph 2 3')
        exit()
    
    # Process command line arguments
    proc_index = int( sys.argv[1] )
    number_of_proc = int( sys.argv[2] )
    
    # Creat list of all pors
    allPorts = [6000 + i for i in range(number_of_proc)]
    
    # Set ports
    local_port =   allPorts[proc_index]
    remote_ports = [x for x in allPorts if x != local_port]
    
    # Create queue for messages from the local server
    queue = Queue()
    
    # Create and start server process
    server = Process(target=server_fun, args=(local_port,queue))
    server.start()
    
    # Set the lst of the addresses of the peer node's servers
    remote_server_addresses = [('localhost', port) for port in remote_ports]
    
    # Send a message to the peer node and receive message from the peer node.
    # To exit send message: exit.
    print('Send a message to the peer node and receive message from the peer node.')
    print('To exit send message: exit.')
    
    while True:
        # Input message
        
        
        if proc_index == 0:        
            msg = input('Enter message: ')
            #print('Message sent: %s \n' % (msg))
            
            message = Mess(0,msg,allPorts[proc_index],remote_ports)

            if msg == 'exit':
                sendMsg( ('localhost', local_port), 'exit')
                break
            
            # Send message to peer node's servers
            broadcastMsg(remote_server_addresses, message)
            
            msgs = rcvMsgs(queue, number_of_proc - 1)
            
            for i in msgs:
                print('Messages received:', i.message)
            
            
        else:
            
            msg = rcvMsg(queue)
            print("QUEEEEE: ",msg.message,msg.src)
            
            message = Mess(0,"PRIMIO",allPorts[proc_index],msg.src)
            
            sendMsg(('localhost', msg.src),message)
    
    # Join with server process
    server.join()
    
    # Delete queue and server
    del queue
    del server

if __name__ == '__main__':
    main()

