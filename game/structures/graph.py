class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = []

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, u, v, w):
        self.edges.append((w, u, v))

    def kruskal(self):
        parent = {n: n for n in self.nodes}

        def find(n):
            if parent[n] != n:
                parent[n] = find(parent[n])
            return parent[n]

        def union(a, b):
            parent[find(a)] = find(b)

        mst = []
        total_cost = 0

        for w, u, v in sorted(self.edges):
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, w))
                total_cost += w

        return mst, total_cost