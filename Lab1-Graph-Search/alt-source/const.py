# cell
COLS, ROWS = 30, 22
CELL_WIDTH = 25
CELL_SPACE = 1 # space between two brick

# screen
BOUND = 15
EMPTY = 290
WIDTH, HEIGHT = 750+2*BOUND + (COLS-1)*CELL_SPACE, 550+2*BOUND + (ROWS-1)*CELL_SPACE
FONT_SIZE = 15

# color
GREY = (100, 100, 100)
WHITE = (255, 255, 255) # moveable
YELLOW = (200, 200, 0) # current node
RED = (255, 0, 0)  # discovered node
BLUE = (30, 144, 255)  # completed node (item of closed set)
PURPLE = (138, 43, 226) # goal
ORANGE = (255,165,0) # start
GREEN = (54, 179, 72) # path
BLACK = (0, 0, 0) # brick

# something else (this is ugly code)
COLOR_DICT = {0: WHITE, 1: BLACK, 2: YELLOW, 3: ORANGE, 4: PURPLE, 5: BLUE, 6: RED, 7: GREEN}
NODE_DICT = {"moveable": 0, "brick": 1, "current": 2, "start": 3, 
             "goal": 4, "completed": 5, "discovered": 6, "path": 7}
STATUS_DICT = {0: "Moveable Node", 1: "Brick Node (not moveable)", 2: "Current Node", 3: "Start Node",
               4: "Goal Node", 5: "Completed Node", 6: "Discovered Node", 7: "Path Node"}