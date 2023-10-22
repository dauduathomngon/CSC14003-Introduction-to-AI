import pygame
import random
from typing import List, Tuple
from const import *

random.seed(2345)

class Node:
    def __init__(self, x, y, a, id, status) -> None:
        """
        (x, y): The position top-left corner of node (a rectangle)
        a: width of node
        id: id of node
        status: status of node (path, brick, current, ...)
        is_change: if a node has changed its status, the renderer will know to render it
        """
        self.x = x
        self.y = y
        self.width = a
        self.id = id
        self.status: str = status
        self.is_change: bool = True
        self.parent: Node = None # father of this node

    def change_status(self, new_status) -> None:
        if self.status != new_status:
            self.is_change = True
            self.status = new_status

class SearchSpace:
    def __init__(self) -> None:
        # create list of all node
        self.grid_cells: List[Node] = []
        self.create_grid()

        # start node and goal node
        self.start: Node = self.grid_cells[0]
        self.goal: Node = self.grid_cells[-1]

        # running state and initial state (use for restart the maze)
        self.is_running = False
        self.initial_state = True 

    def create_grid(self) -> None:        
        for i in range(0, ROWS):
            for j in range(0, COLS):
                # define the brick's appearing
                is_brick = True if random.randint(1,3) == 1 else False
                self.grid_cells.append(Node(j*(CELL_WIDTH + CELL_SPACE) + BOUND,
                                           i*(CELL_WIDTH + CELL_SPACE) + BOUND,
                                           CELL_WIDTH,
                                           i*COLS + j,
                                           "brick" if is_brick else "moveable"))
        self.grid_cells[0].status = "start"
        self.grid_cells[-1].status = "goal" # start and goal always the first and the last

    def restart(self) -> None:
        if not self.is_running and self.initial_state:
            # clear all things
            self.grid_cells = []
            self.create_grid()

    def get_neighbors(self, node: Node) -> list[Node]:
        x, y = node.id % COLS, node.id // COLS

        # define the directions of agent
        up    = (y-1)*COLS + x if y-1 >= 0 else None
        down  = (y+1)*COLS + x if y+1 < ROWS else None
        left  = y*COLS + (x-1) if x-1 >= 0 else None
        right = y*COLS + (x+1) if x+1 < COLS else None

        left_up = (y-1)*COLS + (x-1) if y-1 >= 0 and x-1 >= 0 else None
        left_down = (y+1)*COLS + (x-1) if y+1 < ROWS and x-1 >= 0 else None
        right_up = (y-1)*COLS + (x+1) if y-1 >= 0 and x+1 < COLS else None
        right_down = (y+1)*COLS + (x+1) if y+1 < ROWS and x+1 < COLS else None

        directions = [up, down, left, right, left_up, left_down, right_up, right_down]
        neighbors = []
        for dir_ in directions:
            if dir_ is not None and self.grid_cells[dir_].status != "brick":
                neighbors.append(self.grid_cells[dir_])

        return neighbors

    def get_length(self):
        return len(self.grid_cells)

    def is_goal(self, node: Node) -> bool:
        return node.id == self.goal.id

    def draw_path(self, sc: pygame.Surface, node: Node) -> None:
        current = node
        while current is not None:
            current.change_status("path")
            current = current.parent
            self.draw(sc)

    def draw(self, sc: pygame.Surface) -> None:
        if self.is_running:
            # render all node which has changed
            for node in self.grid_cells:
                if node.is_change:
                    pygame.draw.rect(sc,
                                    COLOR_DICT[NODE_DICT[node.status]],
                                    (node.x, node.y, node.width, node.width))
                    pygame.time.delay(100) # you can change the time node change color here
                    pygame.display.flip()

        elif self.initial_state: # start state
            self.initial_state = False # set initial state to false after draw
            for node in self.grid_cells:
                pygame.draw.rect(sc,
                                COLOR_DICT[NODE_DICT[node.status]],
                                (node.x, node.y, node.width, node.width))

        # set all change status of node to fail 
        for node in self.grid_cells:
            node.is_change = False