import sys
from multiprocessing import Process, Queue
from msg_passing_api import *
import time
import json

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
        self.children = list()
        self.other = list()
      
def readFromJSON():
    d = dict()

    with open("nodes.json", "r") as read_file:
        data = json.load(read_file)
    
    for n in data['Nodes']:
        key = n['id']
        values = n['neighbours']
        d[key] = values
        
    return d
        
def makeNodes(neighbours_dict):
    nodes = list()
    number_of_proc = len(neighbours_dict)
    
    for i in range(0,number_of_proc):
        nodes.append(Node(neighbours_dict[i],i))
        
    return nodes
    
def main():
    # Parse command line arguments
    if len(sys.argv) != 2:
        print('Program usage: Please enter index of process')
        print('Example: project.py 1')
        exit()

    # Process command line arguments
    proc_index = int( sys.argv[1] )
    
    # Create dictionary of all nodes
    neighbours_dict = readFromJSON()                   

    number_of_proc = len(neighbours_dict)
    init_node = 0
    
    # Create list of all pors
    allPorts = [6000 + i for i in range(number_of_proc)]
    neighbours_ports = [6000 + i for i in neighbours_dict[proc_index]]

    # Set ports
    local_port =   allPorts[proc_index]
    remote_ports = [x for x in allPorts if x != local_port]

    # Create nodes
    nodes = makeNodes(neighbours_dict)
    
    # Create queue for messages from the local server
    queue = Queue()

    # Create and start server process
    server = Process(target=server_fun, args=(local_port,queue))
    server.start()

    # Set the lst of the addresses of the peer node's servers
    remote_server_addresses = [('localhost', port) for port in neighbours_ports]

    while True:
        # Input message
        if proc_index == init_node:
            msg = input('Enter message: ')
            
            nodes[proc_index].message = Mess("M",msg,allPorts[proc_index],neighbours_ports)

            # Send message to all neighbours
            broadcastMsg(remote_server_addresses, nodes[proc_index])

            for i in range(0,(len(neighbours_dict[init_node]) - 1)):
                msgs = rcvMsg(queue)
                if msgs.message.type == "P":
                    nodes[proc_index].children.append(msgs.message.src)
                elif msgs.message.type == "A":
                    nodes[proc_index].other.append(msgs.message.src)
            
            sendMsg( ('localhost', local_port), 'exit')
            break

        else:
            print("Waiting for message...")
            msg = rcvMsg(queue)
            print("Received from parent: ", msg.id)
            print("Received message: ",msg.message.message)
            
            nodeTmp = nodes[proc_index]
            nodeTmp.message = msg.message.message

            if(msg.message.type == "M"):
                if(nodeTmp.parent == None):
                    nodeTmp.parent = msg.id
                    messageTmp = nodeTmp.message
                    nodeTmp.message = Mess("P","Parent",allPorts[proc_index],msg.message.src)
                    sendMsg(('localhost', msg.message.src),nodeTmp)

                    for i in nodeTmp.neighbours:
                        if i != nodeTmp.parent:
                            destPortTmp = 6000 + i
                            nodeTmp.message = Mess("M",messageTmp,allPorts[proc_index],destPortTmp)
                            sendMsg(('localhost', destPortTmp),nodeTmp)
                    for j in range(len(nodeTmp.neighbours) - 1):
                        msg2 = rcvMsg(queue)
                        if msg2.message.type == "P":
                            nodeTmp.children.append(msg.message.src)
                        elif msg.message.type == "A":
                            nodeTmp.other.append(msg.message.src)
                else:
                    nodeTmp.parent = msg.id
                    messageTmp = nodeTmp.message
                    nodeTmp.message = Mess("A","Already",allPorts[proc_index],msg.message.src)
                    sendMsg(('localhost', msg.message.src),nodeTmp)
                    
            sendMsg( ('localhost', local_port), 'exit')
            break

    # Join with server process
    server.join()

    # Delete queue and server
    del queue
    del server

if __name__ == '__main__':
    main()
