import pygame
import sys
import click
from typing import List
from const import *
from algo import *
from maze import SearchSpace
from utils import draw_note

class App:
    def __init__(self, algo_input: str, name: str) -> None:
        pygame.init()
        pygame.font.init()

        # general setup
        self.is_running = True
        self.algo = algo_input
        self.space = SearchSpace()
        
        # pygame set up
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH + EMPTY, HEIGHT),
                                              pygame.DOUBLEBUF,
                                              16)

        pygame.display.set_caption(f"{name} - {algo_input}")

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.space.initial_state = True
                    self.space.restart()
                if event.key == pygame.K_RETURN:
                    self.space.is_running = True

    def run(self) -> None:
        self.screen.fill(pygame.color.Color(GREY)) # fill the background with grey color
        draw_note(self.screen) # draw all note in the right of window
        self.space.draw(self.screen) # initial draw
        pygame.display.update() # update display

        # main loop
        while self.is_running:        
            self.handle_event(pygame.event.get())

            if self.space.is_running:
                if self.algo == "DFS":
                    DFS(self.space, self.screen)
                elif self.algo == "BFS":
                    BFS(self.space, self.screen)
                elif self.algo == "UCS":
                    UCS(self.space, self.screen)
                elif self.algo == "AStar":
                    AStar(self.space, self.screen)
                self.space.is_running = False
            else:
                self.space.draw(self.screen) # draw if not running
            
            pygame.display.update()
            self.clock.tick(60)

        # quit the app
        pygame.quit()
        sys.exit()

@click.command()
@click.option('--algo', default = 'DFS', help = "Algorithm for search agent")
@click.option('--name', default = 'Your name here', help = "Your name on title of Pygame")
def cli(algo: str, name: str) -> None:
    app = App(algo, name)
    app.run()

if __name__=='__main__':
    cli()