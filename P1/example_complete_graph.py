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
    def __init__(self,neighbours , id):
        self.id = id
        self.messageType = None
        self.neighbours = neighbours
        self.parent = None
        self.message = None
        self.children = None
        self.other = None

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
    
    
    neighbours_dict = {0 : [3,2],
                       1 : [0,2,3],
                       2 : [0,1,3],
                       3 : [1,2]}

                       
    
    
    neighbours_ports = [6000 + i for i in neighbours_dict[proc_index]]
    
    # Set ports
    local_port =   allPorts[proc_index]
    remote_ports = [x for x in allPorts if x != local_port]
    
    node0 = Node(neighbours_dict[0],0)
    node1 = Node(neighbours_dict[1],1)
    node2 = Node(neighbours_dict[2],2)
    node3 = Node(neighbours_dict[3],3)
    
    nodes = [node0,node1,node2,node3]
    
    # Create queue for messages from the local server
    queue = Queue()
    
    # Create and start server process
    server = Process(target=server_fun, args=(local_port,queue))
    server.start()
    
    # Set the lst of the addresses of the peer node's servers
    remote_server_addresses = [('localhost', port) for port in neighbours_ports]
    
    # Send a message to the peer node and receive message from the peer node.
    # To exit send message: exit.
    print('Send a message to the peer node and receive message from the peer node.')
    print('To exit send message: exit.')
    
    while True:
        # Input message
 
        if proc_index == 0:        
            msg = input('Enter message: ')
            #print('Message sent: %s \n' % (msg))
            
            node0.message = Mess("M",msg,allPorts[proc_index],neighbours_ports)
            
            
            
            # Send message to peer node's servers
            broadcastMsg(remote_server_addresses, node0)
            
            if msg == 'exit':
                sendMsg( ('localhost', local_port), 'exit')
                break
                
            msgs = rcvMsgs(queue, len(neighbours_ports))
            
            
            for i in msgs:
               print('Messages received:', i.message.message,i.message.src)
               print("MESSAGESSSSS: ",i.message.type)

        else:
            
            msg = rcvMsg(queue)
            nodeTmp = nodes[proc_index] 
            print("------ID------",nodeTmp.id)
            
            if(msg.message.type == "M"):
                if(nodeTmp.parent == None):
                    nodeTmp.parent = msg.id
                    messageTmp = nodeTmp.message
                    nodeTmp.message = Mess("P","",allPorts[proc_index],msg.message.src)
                    sendMsg(('localhost', msg.message.src),nodeTmp)
                else:   
                    print("Cao")
                    
            print("QUEEEEE: ",msg.message.message,msg.message.src)
            
            if msg.message.message == 'exit':
                sendMsg( ('localhost', local_port), 'exit')
                break
            
            nodeTmp.message = Mess(0,"PRIMIO",allPorts[proc_index],msg.message.src)
            
            sendMsg(('localhost', msg.message.src),nodeTmp)
    
    # Join with server process
    server.join()
    
    # Delete queue and server
    del queue
    del server

if __name__ == '__main__':
    main()

