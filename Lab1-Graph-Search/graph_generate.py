import graphviz
from collections import defaultdict
import math

def get_cost(q, node):
    for w, val in q:
        if val == node:
            return w
    return -1

def replace_cost(q, node, cost):
    idx = q.index((get_cost(q, node), node))
    q[idx] = (cost, node)

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.heuristic = defaultdict(int)

    def add_edge(self, u, v, weight=0):
        self.graph[u].append((weight, v))
        self.graph[v].append((weight, u))

    def add_heuristic(self, u, heuristic):
        self.heuristic[u] = heuristic

    def first_draw(self, G: graphviz.Graph):
        for node in self.graph.keys():
            for weight, neighbor in self.graph[node]:
                G.edge(str(node), str(neighbor), label=str(weight))
        # đây là màu của node bắt đầu (mặc định là cam)
        G.node(str(list(self.graph.keys())[0]), style="filled", fillcolor="orange")
        # đây là màu của node đích (mặc định là tím)
        G.node(str(list(self.graph.keys())[-1]), style="filled", fillcolor="purple")
        G.render("init", cleanup=True)

    def draw_heuristic(self, G: graphviz.Graph):
        self.restart_graph(G)

        for node in self.graph.keys():
            G.node(name= str(node), label=str(node) + f"\n h={self.heuristic[node]}")

        G.render("init_heuristic", cleanup=True)

    def restart_graph(self, G: graphviz.Graph):
        for node in self.graph.keys():
            G.node(name=str(node), style="filled", fillcolor="white")
        G.node(str(list(self.graph.keys())[0]), style="filled", fillcolor="orange")
        G.node(str(list(self.graph.keys())[-1]), style="filled", fillcolor="purple")

    def draw_DFS(self, G: graphviz.Graph):
        self.restart_graph(G)

        open_set = [list(self.graph.keys())[0]]
        closed_set = []

        i = 0
        # đây là màu của node trong open_set (mặc định là xanh dương)
        # (các thuật toán phía dưới tương tự)
        G.node(str(open_set[0]), style="filled", fillcolor="cyan")
        G.render("DFS/" + str(i))

        while open_set:
            node = open_set.pop(-1)
            closed_set.append(node)
            # đây là màu của node trong closed_set (mặc địch là xanh lá cây)
            # (các thuật toán phía dưới tương tự)
            G.node(str(node), style="filled", fillcolor="green")

            if node == list(self.graph.keys())[-1]:
                i += 1
                G.render("DFS/" + str(i))
                break

            for _, neighbor in sorted(self.graph[node], key=lambda x: x[-1], reverse=True):
                if neighbor not in open_set and neighbor not in closed_set:
                    open_set.append(neighbor)
                    G.node(str(neighbor), style="filled", fillcolor="cyan")

            i += 1
            G.render("DFS/" + str(i))

    def draw_BFS(self, G: graphviz.Graph):
        self.restart_graph(G)

        open_set = [list(self.graph.keys())[0]]
        closed_set = []

        i = 0
        G.node(str(open_set[0]), style="filled", fillcolor="cyan")
        G.render("BFS/" + str(i))

        while open_set:
            node = open_set.pop(0)
            closed_set.append(node)
            G.node(str(node), style="filled", fillcolor="green")

            if node == list(self.graph.keys())[-1]:
                i += 1
                G.render("BFS/" + str(i))
                break

            for _, neighbor in sorted(self.graph[node], key=lambda x: x[-1]):
                if neighbor not in open_set and neighbor not in closed_set:
                    open_set.append(neighbor)
                    G.node(str(neighbor), style="filled", fillcolor="cyan")

            i += 1
            G.render("BFS/" + str(i))

    def draw_UCS(self, G: graphviz.Graph):
        self.restart_graph(G)

        open_set = [(0, list(self.graph.keys())[0])]
        closed_set = []

        i = 0
        G.node(str(open_set[0][-1]), style="filled", fillcolor="cyan")
        G.render("UCS/" + str(i))

        while open_set:
            # sort queue before pop
            open_set = sorted(open_set, key=lambda x : x[0])

            cost, node = open_set.pop(0)
            closed_set.append(node)
            G.node(str(node), style="filled", fillcolor="green")

            if node == list(self.graph.keys())[-1]:
                i += 1
                G.render("UCS/" + str(i))
                break

            for weight, neighbor in sorted(self.graph[node], key=lambda x: x[-1]):
                if get_cost(open_set, neighbor) == -1 and neighbor not in closed_set:
                    open_set.append((weight, neighbor))
                    G.node(str(neighbor), style="filled", fillcolor="cyan")
                elif get_cost(open_set, neighbor) != -1 and get_cost(open_set, neighbor) > cost + weight:
                    replace_cost(open_set, neighbor, cost+weight)
                    G.node(str(neighbor), style="filled", fillcolor="cyan")

            i += 1
            G.render("UCS/" + str(i))

    def draw_AStar(self, G: graphviz.Graph):
        self.restart_graph(G)

        start = list(self.graph.keys())[0]
        g_score = [math.inf] * len(self.graph)
        g_score[start] = 0
        open_set = [(self.heuristic[start], start)]
        closed_set = []

        i = 0
        G.node(str(open_set[0][-1]), style="filled", fillcolor="cyan")
        G.render("AStar/" + str(i))

        while open_set:
            # sort queue before pop
            open_set = sorted(open_set, key=lambda x : x[0])

            _, node = open_set.pop(0)
            closed_set.append(node)
            G.node(str(node), style="filled", fillcolor="green")

            for weight, neighbor in sorted(self.graph[node], key=lambda x: x[-1]):
                temp_score = g_score[node] + weight

                if temp_score < g_score[neighbor]:
                    g_score[neighbor] = temp_score
                    f_score = temp_score + self.heuristic[neighbor]

                    if get_cost(open_set, neighbor) == -1 and neighbor not in closed_set:
                        open_set.append((f_score, neighbor))
                        G.node(str(neighbor), style="filled", fillcolor="cyan")

            i += 1
            G.render("AStar/" + str(i))

    def draw_Greedy(self, G:graphviz.Graph):
        self.restart_graph(G)

        start = list(self.graph.keys())[0]
        open_set = [(self.heuristic[start], start)]
        closed_set = []

        i = 0
        G.node(str(open_set[0][-1]), style="filled", fillcolor="cyan")
        G.render("Greedy/" + str(i))

        while open_set:
            # sort queue before pop
            open_set = sorted(open_set, key=lambda x : x[0])

            _, node = open_set.pop(0)
            closed_set.append(node)
            G.node(str(node), style="filled", fillcolor="green")

            if node == list(self.graph.keys())[-1]:
                i += 1
                G.render("Greedy/" + str(i))
                break

            for _, neighbor in sorted(self.graph[node], key=lambda x: x[-1]):
                if get_cost(open_set, neighbor) == -1 and neighbor not in closed_set:
                    open_set.append((self.heuristic[neighbor], neighbor))
                    G.node(str(neighbor), style="filled", fillcolor="cyan")

            i += 1
            G.render("Greedy/" + str(i))

if __name__ == "__main__":
    # có thể sửa format từ pdf sang png (hoặc ngược lại), dùng pdf sẽ rõ hơn png
    G = graphviz.Graph(format="pdf", strict=True, graph_attr=dict(rankdir='LR'))

    g = Graph()

    # mọi người có thể sửa node lại cho phù hợp, tham số cuối là trọng số.
    g.add_edge(0, 1, 5)
    g.add_edge(0, 2, 2)
    g.add_edge(0, 3, 7)
    g.add_edge(2, 3, 4)
    g.add_edge(3, 4, 5)
    g.add_edge(1, 4, 7)

    # gọi hàm này để vẽ đồ thị
    g.first_draw(G)

    # gọi hàm này để vẽ nhiều trạng thái đồ thị cho từng đợt chạy của thuật toán
    g.draw_BFS(G)
    g.draw_DFS(G)
    g.draw_UCS(G)

    # thêm heurisitc cho từng node
    g.add_heuristic(0, 8)
    g.add_heuristic(1, 5)
    g.add_heuristic(2, 6)
    g.add_heuristic(3, 2)
    g.add_heuristic(4, 0)

    # add heuristic rồi mới gọi hàm draw_heuristic để vẽ đồ thị có heuristic
    g.draw_heuristic(G)

    # rồi sau đó vẽ Greedy với A*
    g.draw_Greedy(G)
    g.draw_AStar(G)