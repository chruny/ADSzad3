from collections import defaultdict
import copy


# This class represents a directed graph using adjacency list representation
class Graph:

    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = defaultdict(list)  # default dictionary to store graph

    # function to add an edge to graph
    def add_edge(self, u, v):
        self.graph[u].append(v)

    def add_edge_inv(self, u, v):
        self.graph[v].append(u)

    def DFSUtil(self, v, visited, arr_grp):
        visited[v - 1] = True
        arr_grp.append(v)
        for i in self.graph[v]:
            if not visited[i - 1]:
                self.DFSUtil(i, visited, arr_grp)
        return arr_grp

    def fill_order(self, v, visited, stack):
        visited[v - 1] = True
        for i in self.graph[v]:
            if not visited[i - 1]:
                self.fill_order(i, visited, stack)
        stack = stack.append(v)

    def get_transpose(self):
        g = Graph(self.V)

        for i in self.graph:
            for j in self.graph[i]:
                g.add_edge(j, i)
        return g

    def get_SCC(self, gr):

        stack = []
        visited = [False] * (self.V)
        for i in range(1, self.V + 1):
            if not visited[i - 1]:
                self.fill_order(i, visited, stack)
        visited = [False] * (self.V)
        arr_arr_grp = []
        while stack:
            i = stack.pop()
            if not visited[i - 1]:
                arr_grp = []
                gr.fill_order(i, visited, arr_grp)
                arr_arr_grp.append(arr_grp)
        if get_satisfiable(arr_arr_grp, self.V):
            get_logical_values2(arr_arr_grp, self.V/2)
        else:
            with open("vystup.txt", "w") as f:
                f.write("Non Satis")
        return arr_arr_grp


def get_satisfiable(arr_scc, n):
    for scc in arr_scc:
        for item in scc:
            if item + n in scc:
                print("Non Satis")
                return False
    else:
        print("Satis")
        return True


def get_max_column(arr_scc):
    max_value = 0
    for i in range(len(arr_scc)):
        if len(arr_scc[i]) > max_value:
            max_value = len(arr_scc[i])
    return max_value


def get_logical_values2(arr_scc, n):
    used_groups = {}
    for x in range(len(arr_scc) - 1, -1, -1):
        check = False
        value = False
        for i in range(len(arr_scc[x]) - 1, -1, -1):
            if arr_scc[x][i] in used_groups:
                check = True
                value = used_groups[arr_scc[x][i]] == "TRUE" and True or False
                if not value:
                    break
        if check and value:
            if value:
                for y in arr_scc[x]:
                    used_groups[y] = "TRUE"
                    if y <= n:
                        used_groups[y + n] = "FALSE"
                    else:
                        used_groups[y - n] = "FALSE"
        elif check and not value:
            for y in arr_scc[x]:
                used_groups[y] = "FALSE"
                if y <= n:
                    used_groups[y + n] = "TRUE"
                else:
                    used_groups[y - n] = "TRUE"
        else:
            for y in arr_scc[x]:
                used_groups[y] = "TRUE"
                if y <= n:
                    used_groups[y + n] = "FALSE"
                else:
                    used_groups[y - n] = "FALSE"
    with open("vystup.txt","w") as f:
        for i in range(1, int(n) + 1):
            f.write("Satis")
            f.write(used_groups[i])
            print(used_groups[i])


def is2Sat(n, m, a, b):
    graph_1 = Graph(2 * n)
    graph_2 = Graph(2 * n)
    for i in range(0, m):
        if a[i] > 0 and b[i] > 0:
            graph_1.add_edge(a[i] + n, b[i])
            graph_2.add_edge_inv(a[i] + n, b[i])
            graph_1.add_edge(b[i] + n, a[i])
            graph_2.add_edge_inv(b[i] + n, a[i])

        elif a[i] > 0 > b[i]:
            graph_1.add_edge(a[i], n - b[i])
            graph_2.add_edge_inv(a[i], n - b[i])
            graph_1.add_edge(-b[i], a[i])
            graph_2.add_edge_inv(-b[i], a[i])

        elif a[i] < 0 < b[i]:
            graph_1.add_edge(-a[i], b[i])
            graph_2.add_edge_inv(-a[i], b[i])
            graph_1.add_edge(b[i] + n, n - a[i])
            graph_2.add_edge_inv(b[i] + n, n - a[i])

        else:
            graph_1.add_edge(-a[i], n - b[i])
            graph_2.add_edge_inv(-a[i], n - b[i])
            graph_1.add_edge(-b[i], n - a[i])
            graph_2.add_edge_inv(-b[i], n - a[i])

    graph_1.get_SCC(graph_2)


with open("vstup.txt") as f:
    line1 = f.readline()
    line1 = line1.split()
    lines = f.readlines()
    matrix = [[0 for x in range(int(line1[1]))] for y in range(2)]

    for i in range(int(line1[1])):
        line = lines[i].split()
        if len(line) == 2:
            matrix[0][i] = int(lines[i].split()[0])
            matrix[1][i] = int(lines[i].split()[0])
        if len(line) == 3:
            matrix[0][i] = int(lines[i].split()[0])
            matrix[1][i] = int(lines[i].split()[1])

    is2Sat(len(matrix), len(matrix[0]), matrix[0], matrix[1])
