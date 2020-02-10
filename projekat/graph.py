
class Vertex:
    def __init__(self,p = None):
        self.parent = p
        self.neighbours = list()

class Graph:
    def __init__(self,ver = None, ed = None):
        self.vertices = ver

def MakeGraph():
    
    n1 = Vertex()
    n2 = Vertex(n = "b")
    n3 = Vertex(n = "c")
    n4 = Vertex(n = "d")
    n5 = Vertex(n = "e")
    n6 = Vertex(n = "f")
    n7 = Vertex(n = "g")

    a.neighbours.append(b)
    a.neighbours.append(c)

    b.neighbours.append(d)

    c.neighbours.append(d)
    c.neighbours.append(d)

    d.neighbours.append(e)
    d.neighbours.append(f)

    e.neighbours.append(f)
    e.neighbours.append(g)

    f.neighbours.append(g)

    # ubacimo sve cvorove u jednu listu cvorova
    v = [a,b,c,d,e,f,g]