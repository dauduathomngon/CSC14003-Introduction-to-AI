import pygame
from maze import SearchSpace

# Note:
# Whenever you add a node to frontier (or open set), change status of this node to "discovered" by calling node.change_status("discovered")
# Whenever you add a note to explored (or closed set), change status of this node to "completed"
# Remember: change status by change_status not calling directly node.status, this will improve the render performance or it will not render :>
# Whenever you choose a node as current, change status to "current" and call g.draw(sc) after (this will be the correct way to render)
# If you want to have path, then you can set a parent for a node by node.parent = "whatever node you want to be parent"
# After finish the algorithm, if you want to render path, call g.draw_path(node) for node you want to trace back (remember to set parent)

def DFS(g: SearchSpace, sc: pygame.Surface):
    frontier = [g.start] # open set
    explored = [] # closed set
    node = None
    while frontier: # is not empty
        node = frontier.pop(-1)
        node.change_status("current")
        g.draw(sc)
        if g.is_goal(node):
            break
        for n in g.get_neighbors(node):
            if n not in explored:
                frontier.append(n)
                n.change_status("discovered")
                n.parent = node
        explored.append(node)
        node.change_status("completed")
    # draw path
    g.draw_path(sc, node)

def BFS(g: SearchSpace, sc: pygame.Surface):
    pass

def UCS(g: SearchSpace, sc: pygame.Surface):
    pass

def AStar(g: SearchSpace, sc: pygame.Surface):
    pass