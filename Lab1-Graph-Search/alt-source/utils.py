import pygame
from const import *

def draw_rect(sc: pygame.Surface, 
              color, 
              width, 
              height):
    pygame.draw.rect(sc, color, (width, height, CELL_WIDTH, CELL_WIDTH))

def draw_text(sc: pygame.Surface, 
              font: pygame.font.Font, 
              color, 
              text: str, 
              height, 
              width):
    sc.blit(font.render(text, True, color), (width, height))

# I know this code looks ugly, so I'm sorry about this :<
def draw_note(sc: pygame.Surface):
    font = pygame.font.SysFont("Arial", FONT_SIZE)

    # draw node guide
    for i in range(0, len(COLOR_DICT)):
        draw_rect(sc, COLOR_DICT[i], WIDTH + CELL_SPACE, HEIGHT - (580 - i*55))
        if i == 5:
            draw_text(sc, font, WHITE, STATUS_DICT[i], 
                      HEIGHT - (580 - i*55) + CELL_SPACE*2.5, WIDTH + CELL_SPACE*10 + CELL_WIDTH)
            draw_text(sc, font, WHITE, "(Discovered and Expanded)", 
                      HEIGHT - (580 - i*55) + CELL_SPACE*(1.5 * FONT_SIZE), WIDTH + CELL_SPACE*10 + CELL_WIDTH)
            continue
        if i == 6:
            draw_text(sc, font, WHITE, STATUS_DICT[i],
                      HEIGHT - (580 - i*55) + CELL_SPACE*2.5, WIDTH + CELL_SPACE*10 + CELL_WIDTH)
            draw_text(sc, font, WHITE, "(Discovered but not yet Expanded)", 
                      HEIGHT - (580 - i*55) + CELL_SPACE*(1.5 * FONT_SIZE), WIDTH + CELL_SPACE*10 + CELL_WIDTH)
            continue
        draw_text(sc, font, WHITE, STATUS_DICT[i], 
                  HEIGHT - (580 - i*55) + CELL_SPACE*5, WIDTH + CELL_SPACE*10 + CELL_WIDTH)

    # draw input guide
    draw_text(sc, font, WHITE, "Press Enter to start algorithm", HEIGHT - 150, WIDTH + 5)
    draw_text(sc, font, WHITE, "Press Space to restart the maze", HEIGHT - (150 - FONT_SIZE*2), WIDTH + 5)
    draw_text(sc, font, WHITE, "From 21TNT1 with love <3", HEIGHT - (150 - FONT_SIZE*5), WIDTH + 5)
    draw_text(sc, font, WHITE, "Source: baolongnguyen.mac@gmail.com", HEIGHT - (150 - FONT_SIZE*7), WIDTH + 5)