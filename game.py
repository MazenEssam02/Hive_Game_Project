import pygame
import sys
from constant import WIDTH, HEIGHT, WHITE, RADIUS
from hex import draw_grid #, get_cords
# init pygame
pygame.init()

# set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello World")
# fill screen with white
screen.fill(WHITE)

# draw grid
tiles = draw_grid(screen, rows=20, cols=23)
for tile in tiles:
    print(tile.cord)
# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # update the display
    pygame.display.flip()
# quit pygame

pygame.quit()
sys.exit()
