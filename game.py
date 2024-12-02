import pygame
import sys
from Model import QueenBee
from inventory import Inventory_Frame
from constant import WIDTH, HEIGHT, WHITE, TIMER_EVENT
from hex import draw_grid, get_clicked_hex
from turn import turn_terminal
from state import state
# init pygame
pygame.init()

# init game state

game = state('WHITE TURN')
time_left = 3
# set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hive Game")

# draw grid
tiles = draw_grid(screen, rows=16, cols=19)
white_inventory = Inventory_Frame((0, 158), 0, white=True)
black_inventory = Inventory_Frame((400, 158), 1, white=False)
white_tiles = white_inventory.draw(screen)
black_tiles = black_inventory.draw(screen)
background = pygame.Surface(screen.get_size())

# Draw turn panel
# white_panel = turn((0,0) , 'White')
# black_panel = turn((screen.get_width() - 100,0) , 'black')
turn_panel = turn_terminal((screen.get_width() // 2 - 150, 0))
selected_tile = None

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_tile = get_clicked_hex(
                screen, tiles+white_tiles+black_tiles, mouse_pos)

            if clicked_tile:
                if selected_tile is None:
                    if clicked_tile.has_pieces():
                        selected_tile = clicked_tile
                        selected_tile.highlight()
                        for move in selected_tile.pieces[-1].valid_moves():
                            for tile in tiles:
                                if move == tile.position:
                                    tile.highlight()

                else:
                    selected_tile.move_piece(clicked_tile)
                    selected_tile.unhighlight()
                    selected_tile = None
                    for tile in tiles:
                        tile.unhighlight()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        # elif event.type == TIMER_EVENT and time_left < 0:
    screen.fill(WHITE)
    for tile in tiles:
        tile.draw(screen)

    white_inventory.draw(screen)
    black_inventory.draw(screen)

    # Draw turn panel
    # white_panel.draw(screen)
    # black_panel.draw(screen)
    turn_panel.draw(screen, 'BLACK TURN')
    pygame.display.flip()

# quit pygame

pygame.quit()
sys.exit()
