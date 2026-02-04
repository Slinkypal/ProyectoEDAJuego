class pathfinding:
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
