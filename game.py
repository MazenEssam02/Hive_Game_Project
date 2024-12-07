import pygame
import sys
from Menus import start_menu, opponent_menu, difficulty_menu, end_menu
from inventory import Inventory_Frame
from constant import WIDTH, HEIGHT, WHITE, TIMER_EVENT
from hex import draw_grid, get_clicked_hex, generate_tile_dict
from turn import turn_terminal
from state import state, TurnTimer
from Controller import get_valid_moves, is_queen_surrounded, get_all_valid_moves_for_color
# init pygame
pygame.init()

# init game state
game = state()
timer = TurnTimer()
# set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hive Game")
tiles = []
tile_dict = {}
white_inventory = None
black_inventory = None
turn_panel = None
all_tiles = []
selected_tile = None
loser_color = None


def init():
    # draw grid
    global tiles, tile_dict, white_inventory, black_inventory, all_tiles, turn_panel, selected_tile, all_tile_dict
    tiles = draw_grid(screen, rows=16, cols=19)
    tile_dict = generate_tile_dict(tiles)
    white_inventory = Inventory_Frame((0, 170), 0, white=True)
    black_inventory = Inventory_Frame((400, 170), 1, white=False)
    white_tiles = white_inventory.draw(screen)
    black_tiles = black_inventory.draw(screen)
    all_tiles = tiles + white_tiles + black_tiles
    all_tile_dict = generate_tile_dict(all_tiles)

    turn_panel = turn_terminal((screen.get_width() // 2 - 150, 0), 'WHITE')
    selected_tile = None
    loser_color = None


init()
while game.running:
    if game.play_new_game:
        init()
        game.start_opponent_menu()
    while game.menu_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                game.quit()

        start_menu(screen, game)
        pygame.time.Clock().tick(60)
        pygame.display.flip()
    while game.opponent_menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                game.quit()
        opponent_menu(screen, game)
        pygame.time.Clock().tick(60)
        pygame.display.flip()
    while game.difficulitiy_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
        difficulty_menu(screen, game)
        pygame.time.Clock().tick(60)
        pygame.display.flip()
    while game.main_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(get_all_valid_moves_for_color(game, all_tiles, all_tile_dict))
                mouse_pos = pygame.mouse.get_pos()
                clicked_tile = get_clicked_hex(screen, all_tiles, mouse_pos)
                if clicked_tile:
                    if selected_tile is None:
                        if clicked_tile.pieces:
                            # Check if the piece belongs to the current player
                            piece = clicked_tile.pieces[-1]
                            if game.current_state == piece.color:
                                selected_tile = clicked_tile
                                selected_tile.selected()
                                valid_moves = get_valid_moves(
                                    piece, game, tiles, tile_dict)
                                for move in valid_moves:
                                    for tile in tiles:
                                        if move == tile.position:
                                            tile.highlight()
                    else:
                        if selected_tile != clicked_tile and clicked_tile.position in valid_moves:
                            selected_tile.move_piece(clicked_tile)
                            queen_color = is_queen_surrounded(piece, tile_dict)
                            if queen_color:
                                
                                loser_color = queen_color
                                game.start_end_loop()
                                pygame.time.delay(200)

                            game.change_turn()
                            turn_panel.update(screen, game.current_state)
                            timer.reset_timer()
                        selected_tile.unhighlight()
                        selected_tile = None
                        for tile in tiles:
                            tile.unhighlight()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:

                    game.quit()
            elif event.type == TIMER_EVENT:
                if timer.get_time() <= 0:
                    game.change_turn()
                    game.turn -= 1
                    selected_tile.unhighlight()
                    selected_tile = None
                    for tile in tiles:
                            tile.unhighlight()
                    turn_panel.update(screen, game.current_state)
                    timer.reset_timer()
                else:
                    timer.update_timer()
        screen.fill(WHITE)
        for tile in tiles:
            tile.draw(screen)

        white_inventory.draw(screen)
        black_inventory.draw(screen)

        turn_panel.draw(screen, timer.get_time())
        pygame.time.Clock().tick(60)
        pygame.display.flip()
    while game.end_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                game.quit()
        end_menu(screen, game, loser_color)
        pygame.time.Clock().tick(60)
        pygame.display.flip()

# quit pygame
pygame.quit()
sys.exit()
