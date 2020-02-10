import sys
from multiprocessing import Process, Queue
from msg_passing_api import *

class Vertex:
    def __init__(self,p):
        self.parent = p
        self.neighbours = list()

class Graph:
    def __init__(self,ver = None):
        self.vertices = ver
        
def printGraph(g):
    for i in g.vertices:
        print("MOJ ID: ",i.parent)
        for j in i.neighbours:
            print("KOMSIJA: ",j.parent)
        
def MakeGraph():
    
    n1 = Vertex(1)
    n2 = Vertex(2)
    n3 = Vertex(3)
    n4 = Vertex(4)
    n5 = Vertex(5)
    n6 = Vertex(6)
    n7 = Vertex(7)

    n1.neighbours.append(n2)
    n1.neighbours.append(n3)
    n1.neighbours.append(n4)
    
    v = [n1,n2,n3,n4,n5,n6,n7]
    
    g = Graph(v)

    return g


def spanning(neighbours,):
    parent = int( sys.argv[1])
    
    number_of_proc = int( sys.argv[2] )
    
    # Creat list of all pors
    allPorts = [6000 + i for i in range(number_of_proc)]
    
    # Set ports
    local_port_server = allPorts[parent]
    
def main():
    graph = MakeGraph()
    printGraph(graph)
    

if __name__ == '__main__':
    main()
