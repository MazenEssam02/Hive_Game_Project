import pygame
import sys
from Model import QueenBee
from inventory import Inventory_Frame
from constant import WIDTH, HEIGHT, WHITE
from hex import draw_grid, get_clicked_hex
# init pygame
pygame.init()

# set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hive Game")

# draw grid
tiles = draw_grid(screen, rows=16, cols=19)
white_inventory = Inventory_Frame((0, 158), 0, white=True)
black_inventory = Inventory_Frame((400, 158), 1, white=False)
white_tiles=white_inventory.draw(screen)
black_tiles=black_inventory.draw(screen)
background = pygame.Surface(screen.get_size())

selected_tile = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_tile = get_clicked_hex(screen, tiles+white_tiles+black_tiles, mouse_pos)

            if clicked_tile:
                if selected_tile is None:
                    if clicked_tile.has_pieces():
                        selected_tile = clicked_tile
                        for move in selected_tile.pieces[-1].valid_moves():
                            for tile in tiles:
                                if move == tile.position:
                                    tile.highlight()

                else:
                    selected_tile.move_piece(clicked_tile)
                    selected_tile = None
                    for tile in tiles:
                        tile.unhighlight()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill(WHITE)
    for tile in tiles:
        tile.draw(screen)
    
    white_inventory.draw(screen)
    black_inventory.draw(screen)
    pygame.display.flip()

# quit pygame

pygame.quit()
sys.exit()
