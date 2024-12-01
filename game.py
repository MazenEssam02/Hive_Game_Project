import pygame
import sys
from Model import QueenBee, Beetle, Grasshopper, Spider, SoldierAnt
from constant import WIDTH, HEIGHT, WHITE, RADIUS
from hex import draw_grid
# init pygame
pygame.init()

# set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello World")
# fill screen with white
screen.fill(WHITE)

# draw grid
tiles = draw_grid(screen, rows=16, cols=19)
QueenBee1 = QueenBee("White")
QueenBee1.draw(screen, tiles[141].center)
# for tile in tiles:
#     print(tile.position)
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
