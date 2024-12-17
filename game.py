import threading
import pygame
import sys
import copy
from Menus import start_menu, opponent_menu, difficulty_menu, end_menu
from inventory import Inventory_Frame
from constant import WIDTH, HEIGHT, WHITE, TIMER_EVENT
from hex import draw_grid, get_clicked_hex, generate_tile_dict
import hex
from turn import turn_terminal
from state import state, TurnTimer
from Controller import is_queen_surrounded, human_move, get_all_valid_moves_for_color
from AI import AI

pygame.init() # init pygame
game = state() # init game state
timer = TurnTimer() # init timer
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # set up the screen
pygame.display.set_caption("Hive Game")
# initiating variables
tiles = []
temp_tiles = []
white_inventory = None
black_inventory = None
temp_white_inventory = None
temp_black_inventory = None
turn_panel = None
all_tiles = []
selected_tile = None
loser_color = None
valid_moves = None
piece = None
ai_player_black_easy = AI("BLACK", 1)
ai_player_black_medium = AI("BLACK", 2)
ai_player_black_hard = AI("BLACK", 3)
ai_player_white_easy = AI("WHITE", 1)
ai_player_white_medium = AI("WHITE", 2)
ai_player_white_hard = AI("WHITE", 3)


# AI move flag
ai_move_in_progress = False
ai_result = None
ai_lock = threading.Lock()


def ai_thread_function(ai_player, game, tiles, tile_dict, all_tiles, all_tile_dict):
    global ai_result
    ai_result = ai_player.ai_move(
        game, tiles, tile_dict, all_tiles, all_tile_dict)


def init():
    global tiles, tile_dict, white_inventory, black_inventory, temp_white_inventory, temp_black_inventory,all_tiles, turn_panel, selected_tile, all_tile_dict, loser_color
    tiles = draw_grid(screen, rows=16, cols=19) # draw grid
    tile_dict = generate_tile_dict(tiles)
    white_inventory = Inventory_Frame((0, 170), 0, white=True)
    black_inventory = Inventory_Frame((400, 170), 1, white=False)
    temp_white_inventory = Inventory_Frame((0, 170), 0, white=True)
    temp_black_inventory = Inventory_Frame((400, 170), 1, white=False)
    white_tiles = white_inventory.draw(screen)
    black_tiles = black_inventory.draw(screen)
    all_tiles = tiles + white_tiles + black_tiles
    all_tile_dict = generate_tile_dict(all_tiles)
    hex.white_queen_position = None
    hex.black_queen_position = None
    turn_panel = turn_terminal((screen.get_width() // 2 - 150, 0), 'WHITE')
    selected_tile = None
    loser_color = None


init()
while game.running:
    # check if the player wants to play a new game init the game again
    if game.play_new_game:
        init()
        game.start_opponent_menu()
    # Menu game loop
    while game.menu_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                game.quit()

        start_menu(screen, game)
        pygame.time.Clock().tick(60)  # 60 frames per second for better experience
        pygame.display.flip()
    # Opponent menu game loop
    while game.opponent_menu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                game.quit()
        opponent_menu(screen, game)
        pygame.time.Clock().tick(60)  # 60 frames per second for better experience
        pygame.display.flip()
    # Difficulty menu game loop
    while game.difficulitiy_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()

        difficulty_menu(screen, game)
        pygame.time.Clock().tick(60)  # 60 frames per second for better experience
        pygame.display.flip()
    # Main game loop
    while game.main_loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.quit()
            elif event.type == TIMER_EVENT:
                with ai_lock:
                    if timer.get_time() <= 0:

                        game.time_up = True
                    else:
                        timer.update_timer()
            elif (game.selected_opponent == "Human vs Human" or
                  (game.selected_opponent == "Human vs Computer" and game.current_state == "WHITE")):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_tile = get_clicked_hex(
                        screen, all_tiles, mouse_pos)
                    if clicked_tile:
                        (selected_tile, loser_color, valid_moves, piece) = human_move(
                            game, tiles, tile_dict, clicked_tile, selected_tile, loser_color, turn_panel, screen, timer, valid_moves, piece
                        )
                        if game.is_game_over:
                            game.start_end_loop()
                        temp_white_inventory.tiles = copy.deepcopy(white_inventory.tiles)
                        temp_black_inventory.tiles = copy.deepcopy(black_inventory.tiles)
                        temp_tiles = copy.deepcopy(tiles)
                if game.time_up:
                    game.change_turn()
                    game.turn -= 1
                    if selected_tile:
                        selected_tile.unhighlight()
                        selected_tile = None
                    for tile in tiles:
                        tile.unhighlight()
                    turn_panel.update(screen, game.current_state)
                    timer.reset_timer()

        if ((game.selected_opponent == "Human vs Computer" and game.current_state == "BLACK") or
                (game.selected_opponent == "Computer vs Computer")) and not ai_move_in_progress:

            with ai_lock:
                ai_move_in_progress = True  # Prevent other AI threads from starting

            # Select the appropriate AI player based on the current state
            if game.current_state == "BLACK" and game.selected_difficulty == "Easy":
                ai_player = ai_player_black_easy
            elif game.current_state == "BLACK" and game.selected_difficulty == "Medium":
                ai_player = ai_player_black_medium
            elif game.current_state == "BLACK" and game.selected_difficulty == "Hard":
                ai_player = ai_player_black_hard
            elif game.current_state == "WHITE" and game.selected_difficulty == "Easy":
                ai_player = ai_player_white_easy
            elif game.current_state == "WHITE" and game.selected_difficulty == "Medium":
                ai_player = ai_player_white_medium
            elif game.current_state == "WHITE" and game.selected_difficulty == "Hard":
                ai_player = ai_player_white_hard

            # Start the AI thread
            ai_thread = threading.Thread(target=ai_thread_function, args=(
            ai_player, game, tiles, tile_dict, all_tiles, all_tile_dict), daemon=True)
            ai_thread.start()

        # Apply AI result if ready
        with ai_lock:
            if ai_result is not None:
                piece, old_tile, new_tile = ai_result
                old_tile.move_piece(new_tile)
                temp_white_inventory.tiles = copy.deepcopy(white_inventory.tiles)
                temp_black_inventory.tiles = copy.deepcopy(black_inventory.tiles)
                temp_tiles = copy.deepcopy(tiles)
                ai_result = None  # Reset the result
                queen_color = is_queen_surrounded(
                    game.current_state, tile_dict)[0]
                if queen_color:
                    loser_color = queen_color
                    game.is_game_over = True
                    game.start_end_loop()
                else:
                    game.change_turn()
                    turn_panel.update(screen, game.current_state)
                    timer.reset_timer()
                ai_move_in_progress = False  # Allow AI to start on the next turn
        # Rendering logic
        screen.fill(WHITE)
        if ai_move_in_progress:
            for tile in temp_tiles:
                tile.draw(screen)
            temp_white_inventory.draw(screen)
            temp_black_inventory.draw(screen)
            turn_panel.draw(screen, timer.get_time())
        else:
            for tile in tiles:
                tile.draw(screen)
            white_inventory.draw(screen)
            black_inventory.draw(screen)
            turn_panel.draw(screen, timer.get_time())
        pygame.display.flip()
        pygame.time.Clock().tick(60)  # 60 frames per second for better experience

    # End game loop
    while game.end_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                game.quit()
        end_menu(screen, game, loser_color)
        pygame.time.Clock().tick(60)  # 60 frames per second for better experience
        pygame.display.flip()

# quit pygame
pygame.quit()
sys.exit()
