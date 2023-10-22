import pygame
import math
from maze import SearchSpace, Node
from const import *
from typing import List, Tuple

def DFS(g: SearchSpace, sc: pygame.Surface): # Done
    print('Implement DFS algorithm')

    # open_set = [g.start.id]
    # closed_set = []
    # father = [-1]*g.get_length()

    open_set: List[Node] = [g.start]
    closed_set: List[Node] = [] # as a stack
    father: List[Node] = [None]*g.get_length()
    node: Node = g.start # current node

    while open_set: # is not empty
        node = open_set.pop(-1) # LIFO
        node.set_color(YELLOW, sc)

        if g.is_goal(node): # if node is goal
            break

        for neighbor in g.get_neighbors(node):
            if neighbor not in closed_set and neighbor not in open_set:
                open_set.append(neighbor) # to expanded and explored next
                neighbor.set_color(RED, sc)
                father[neighbor.id] = node

        closed_set.append(node) # already expanded and explored
        node.set_color(BLUE, sc)

    # trace path
    trace_path(sc, g, node, father)

    #raise NotImplementedError('not implemented')

def BFS(g: SearchSpace, sc: pygame.Surface):
    print('Implement BFS algorithm')

    open_set = [g.start]
    closed_set = []
    father = [None]*g.get_length()
    node = g.start

    while open_set:
        node = open_set.pop(0)
        node.set_color(YELLOW, sc)

        if g.is_goal(node):
            break

        for neighbor in g.get_neighbors(node):
            if neighbor not in closed_set and neighbor not in open_set:
                open_set.append(neighbor)
                neighbor.set_color(RED, sc)
                father[neighbor.id] = node

        closed_set.append(node)
        node.set_color(BLUE, sc)
        
    trace_path(sc, g, node, father)

    #raise NotImplementedError('not implemented')

def UCS(g: SearchSpace, sc: pygame.Surface):
    print('Implement UCS algorithm')

    # +1 respect if you can implement UCS with a priority queue
    # open_set = [(0, g.start.id)]
    # closed_set = []
    # father = [-1]*g.get_length()
    # cost = [100_000]*g.get_length()
    # cost[g.start.id] = 0

    node = g.start
    father = [None]*g.get_length()
    frontier = PriorityQueue()
    frontier.enqueue(0, node)
    explored_set = []

    while not frontier.is_empty():
        node_cost, node = frontier.dequeue()
        node.set_color(YELLOW, sc)

        if g.is_goal(node):
            break

        explored_set.append(node)
        node.set_color(BLUE, sc)

        for neighbor in g.get_neighbors(node):
            cost = node_cost + get_weight(g, node, neighbor)

            if neighbor not in explored_set and not frontier.is_in(neighbor):
                frontier.enqueue(cost, neighbor)
                neighbor.set_color(RED, sc)
                father[neighbor.id] = node
            
            elif frontier.is_in(neighbor) and cost < frontier.get_cost(neighbor):
                frontier.replace_cost(neighbor, cost)
                father[neighbor.id] = node

    trace_path(sc, g, node, father)
    #raise NotImplementedError('not implemented')

def AStar(g: SearchSpace, sc: pygame.Surface):
    print('Implement AStar algorithm')

    # +1 respect if you can implement AStar with a priority queue
    # open_set = [(0, g.start.id)]
    # closed_set = []
    # father = [-1]*g.get_length()
    # cost = [100_000]*g.get_length()
    # cost[g.start.id] = 0

    father = [None]*g.get_length()
    node = g.start
    cost_set = [math.inf]*g.get_length()
    cost_set[node.id] = 0
    open_set = PriorityQueue()
    closed_set = []

    # A* selects a path that minimizes
    # f(n) = g(n) + h(n)
    # where f(n) is total cost to move from current node to n
    # h(n) is heuristic function, in this case, h(n) = chebyshev distance from n to goal
    # g(n) is cheapest cost of start node to n
    # In the start node, g(n) = 0 so f(n) = h(n)
    open_set.enqueue(distance_to_goal(g, node), node)

    while not open_set.is_empty():
        _, node = open_set.dequeue()
        node.set_color(YELLOW, sc)

        closed_set.append(node)
        node.set_color(BLUE, sc)

        if g.is_goal(node):
            break

        for neighbor in g.get_neighbors(node):
            temp_score = cost_set[node.id] + get_weight(g, node, neighbor)

            if temp_score < cost_set[neighbor.id]:
                father[neighbor.id] = node
                cost_set[neighbor.id] = temp_score
                f_score = temp_score + distance_to_goal(g, neighbor)

                if not open_set.is_in(neighbor) and neighbor not in closed_set:
                    open_set.enqueue(f_score, neighbor)
                    neighbor.set_color(RED, sc)

    trace_path(sc, g, node, father)

    #raise NotImplementedError('not implemented')

def Greedy(g: SearchSpace, sc: pygame.Surface): # Greedy Best-First Search
    node = g.start
    closed_set = []
    father = [None]*g.get_length()

    open_set = PriorityQueue()
    # heuristic function as the distance from node to goal
    open_set.enqueue(distance_to_goal(g, node), node)

    while not open_set.is_empty():
        _, node = open_set.dequeue()
        node.set_color(YELLOW, sc)

        closed_set.append(node)
        node.set_color(BLUE, sc)

        if g.is_goal(node):
            break

        for neighbor in g.get_neighbors(node):
            if neighbor not in closed_set and not open_set.is_in(neighbor):
                open_set.enqueue(distance_to_goal(g, neighbor), neighbor)
                neighbor.set_color(RED, sc)
                father[neighbor.id] = node

    trace_path(sc, g, node, father)

# sort by ascending order, min cost appear first
class PriorityQueue:
    def __init__(self) -> None:
        self.q = [] # [(cost1, node1), (cost2, node2), ...]
        
    def enqueue(self, cost, node: Node) -> None:
        """
        - Insert an element to its correct position
        - Order by its cost
        - Use Naive implementation
        """
        for i, e in enumerate(self.q):
            if cost < e[0]:
                self.q.insert(i, (cost, node))
                return
        self.q.append((cost, node))
        
    def dequeue(self) -> Tuple[int, Node]:
        """
        Return a tuple of node and its cost
        """
        return self.q.pop(0)

    def is_empty(self) -> bool:
        """
        Check if priority queue is empty
        """
        return len(self.q) == 0

    def is_in(self, val: Node) -> bool:
        """
        Check if a node is already in priority queue
        """
        for _, node in self.q:
            if node.id == val.id:
                return True
        return False

    def get_cost(self, val: Node) -> bool:
        """
        Get cost of input node in priority queue
        If it is not in queue, return -1
        """
        for w, n in self.q:
            if n.id == val.id:
                return w
        return -1

    def replace_cost(self, val: Node, weight) -> None:
        """
        Replace the weight of input node in queue
        """
        self.q.remove((self.get_cost(val), val))
        self.enqueue(weight, val)

def get_direction(node: Node):
    x, y = node.id%COLS, node.id//COLS

    # define the directions of agent
    up    = (y-1)*COLS + x if y-1 >= 0 else None
    down  = (y+1)*COLS + x if y+1 < ROWS else None
    left  = y*COLS + (x-1) if x-1 >= 0 else None
    right = y*COLS + (x+1) if x+1 < COLS else None

    left_up = (y-1)*COLS + (x-1) if y-1 >= 0 and x-1 >= 0 else None
    left_down = (y+1)*COLS + (x-1) if y+1 < ROWS and x-1 >= 0 else None
    right_up = (y-1)*COLS + (x+1) if y-1 >= 0 and x+1 < COLS else None
    right_down = (y+1)*COLS + (x+1) if y+1 < ROWS and x+1 < COLS else None

    return [up, down, left, right, left_up, left_down, right_up, right_down]

def get_weight(g: SearchSpace, u: Node, v: Node):
    """
    - Get the weight from node u to v
    - Calculate by assign weight for each direction, because the goal is at bottom right of screen so right_down will be least expensive
    """
    direction_weight = {"up": 6, "down": 3, "left": 7,
                        "right": 2, "left_up": 8, "left_down": 5,
                        "right_up": 4, "right_down": 1}
    direction = ["up", "down", "left", "right",
                 "left_up", "left_down", "right_up", "right_down"]
    direction_value = get_direction(u)

    return direction_weight[direction[direction_value.index(v.id)]]

def trace_path(sc: pygame.Surface, g: SearchSpace, node: Node, father: List[Node]):
    # set color start and goal
    g.start.set_color(ORANGE, sc)
    g.goal.set_color(PURPLE, sc)

    current = node

    while father[current.id] is not None:

        middle_current = (current.rect.x + A/2, current.rect.y + A/2)
        middle_father = (father[current.id].rect.x + A/2, father[current.id].rect.y + A/2)

        pygame.draw.line(sc, WHITE, 
                        start_pos=middle_current,
                        end_pos=middle_father,
                        width=2)
        pygame.display.update()

        current = father[current.id]

def distance_to_goal(g: SearchSpace, node: Node):
    """
    Use chebyshev distance to calculate distance from input node to goal
    """
    return max(abs(node.rect.x - g.goal.rect.x), abs(node.rect.y - g.goal.rect.y))