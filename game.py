import pygame
import sys
from Model import QueenBee
from constant import WIDTH, HEIGHT, WHITE
from hex import draw_grid, get_clicked_hex
# init pygame
pygame.init()

# set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello World")

# draw grid
tiles = draw_grid(screen, rows=16, cols=19)
QueenBee1 = QueenBee("White")
tiles[141].add_piece(QueenBee1)

selected_tile = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_tile = get_clicked_hex(screen, tiles, mouse_pos)

            if clicked_tile:
                if selected_tile is None:
                    if clicked_tile.has_pieces():
                        selected_tile = clicked_tile
                else:
                    selected_tile.move_piece(clicked_tile)
                    selected_tile = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(WHITE)
    for tile in tiles:
        tile.draw(screen)
    # update the display
    pygame.display.flip()
# quit pygame

pygame.quit()
sys.exit()

