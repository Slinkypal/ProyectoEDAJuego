class Graph:
    def __init__(self):
        self.nodes=set()
        self.edges=[]
    def add_node(self,n):
        self.nodes.add(n)
    def add_edge(self,u,v,w):
        self.edges.append((w,u,v))
