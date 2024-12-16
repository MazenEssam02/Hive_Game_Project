import pygame
import sys
from Menus import start_menu, opponent_menu, difficulty_menu, end_menu
from inventory import Inventory_Frame
from constant import WIDTH, HEIGHT, WHITE, TIMER_EVENT
from hex import draw_grid, get_clicked_hex, generate_tile_dict
import hex
from turn import turn_terminal
from state import state, TurnTimer
from Controller import is_queen_surrounded, human_move, get_all_valid_moves_for_color
from AI import AI
# init pygame
pygame.init()

# init game state
game = state()
timer = TurnTimer()
# set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hive Game")
tiles = []
# tile_dict = {}
white_inventory = None
black_inventory = None
turn_panel = None
all_tiles = []
selected_tile = None
loser_color = None
valid_moves = None
piece = None
ai_player_black = AI("BLACK", 1)
ai_player_white = AI("WHITE",1)

import threading

# AI move flag
ai_move_in_progress = False
ai_result = None
ai_lock = threading.Lock()

def ai_thread_function(ai_player, game, tiles, tile_dict, all_tiles, all_tile_dict):
    global ai_result
    
    ai_result = ai_player.ai_move(game, tiles, tile_dict, all_tiles, all_tile_dict)
    print(ai_result[0])
def init():
    # draw grid
    global tiles, tile_dict, white_inventory, black_inventory, all_tiles, turn_panel, selected_tile, all_tile_dict, loser_color
    tiles = draw_grid(screen, rows=16, cols=19)
    tile_dict = generate_tile_dict(tiles)
    white_inventory = Inventory_Frame((0, 170), 0, white=True)
    black_inventory = Inventory_Frame((400, 170), 1, white=False)
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
                pygame.quit()
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
                    clicked_tile = get_clicked_hex(screen, all_tiles, mouse_pos)
                    if clicked_tile:
                        (selected_tile, loser_color, valid_moves, piece) = human_move(
                            game, tiles, tile_dict, clicked_tile, selected_tile, loser_color, turn_panel, screen, timer, valid_moves, piece
                        )
                        if game.is_game_over:
                            game.start_end_loop()
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
            (game.selected_opponent == "Computer vs Computer" )) and not ai_move_in_progress:
            
            with ai_lock:
                ai_move_in_progress = True  # Prevent other AI threads from starting
            
            # Select the appropriate AI player based on the current state
            if game.current_state == "BLACK":
                ai_player = ai_player_black
            elif game.current_state == "WHITE":
                ai_player = ai_player_white
            
            # Start the AI thread
            threading.Thread(target=ai_thread_function, args=(ai_player, game, tiles, tile_dict, all_tiles, all_tile_dict)).start()
        
        # 3. Apply AI result if ready
        with ai_lock:
            if ai_result is not None:
                piece, old_tile, new_tile = ai_result
                print(old_tile.position, new_tile.position)
                old_tile.move_piece(new_tile)
                ai_result = None  # Reset the result
                queen_color = is_queen_surrounded(game.current_state, tile_dict)[0]
                if queen_color:
                    loser_color = queen_color
                    game.is_game_over = True
                    game.start_end_loop()
                else:
                    game.change_turn()
                    turn_panel.update(screen, game.current_state)
                    timer.reset_timer()
                ai_move_in_progress = False  # Allow AI to start on the next turn
        # 4. Rendering logic
        
        screen.fill(WHITE)
        for tile in tiles:
            tile.draw(screen)
        white_inventory.draw(screen)
        black_inventory.draw(screen)
        turn_panel.draw(screen, timer.get_time())
        pygame.display.flip()
        pygame.time.Clock().tick(60)  # 60 frames per second for better experience

    # while game.main_loop:
    #     for event in pygame.event.get():
    #         if get_all_valid_moves_for_color(game, tiles, tile_dict, all_tiles, game.current_state) == {}:
    #             game.change_turn()
    #             turn_panel.update(screen, game.current_state)
    #             timer.reset_timer()
    #         if event.type == pygame.QUIT:
    #             game.quit()
    #         if game.selected_opponent =="Human vs Computer" and game.current_state == 'BLACK':
    #             (piece,tile,new_tile)=ai_player_black.ai_move(game, tiles,tile_dict,all_tiles, all_tile_dict)
    #             tile.move_piece(new_tile)
    #             queen_color = is_queen_surrounded(game.current_state, tile_dict)[0]
    #             if queen_color:
    #                 loser_color = queen_color
    #                 game.is_game_over = True
    #                 pygame.time.delay(200)
    #                 game.start_end_loop()
    #             game.change_turn()
    #             turn_panel.update(screen, game.current_state)
    #             timer.reset_timer()
    #         elif game.selected_opponent =="Computer vs Computer" and (game.current_state == 'BLACK'or game.current_state == 'WHITE'):
    #             if game.current_state == "BLACK":
    #                 (piece,tile, new_tile) = ai_player_black.ai_move(game, tiles, tile_dict, all_tiles, all_tile_dict)
    #                 tile.move_piece(new_tile)
    #                 queen_color = is_queen_surrounded(game.current_state, tile_dict)[0]
    #                 if queen_color:
    #                     loser_color = queen_color
    #                     game.is_game_over = True
    #                     pygame.time.delay(200)
    #                     game.start_end_loop()
    #                 game.change_turn()
    #                 turn_panel.update(screen, game.current_state)
    #                 timer.reset_timer()
    #             elif game.current_state == "WHITE":
    #                 (piece,tile, new_tile) = ai_player_white.ai_move(game, tiles, tile_dict, all_tiles, all_tile_dict)
    #                 tile.move_piece(new_tile)
    #                 queen_color = is_queen_surrounded(game.current_state, tile_dict)[0]
    #                 if queen_color:
    #                     loser_color = queen_color
    #                     game.is_game_over = True
    #                     pygame.time.delay(200)
    #                     game.start_end_loop()
    #                 game.change_turn()
    #                 turn_panel.update(screen, game.current_state)
    #                 timer.reset_timer()
    #         elif game.selected_opponent=="Human vs Human" or(game.selected_opponent=="Human vs Computer"):
    #             if event.type == pygame.MOUSEBUTTONDOWN:
    #                 mouse_pos = pygame.mouse.get_pos()
    #                 clicked_tile = get_clicked_hex(screen, all_tiles, mouse_pos)
    #                 if clicked_tile:
    #                     (selected_tile, loser_color, valid_moves, piece) = human_move(game, tiles, tile_dict,clicked_tile, selected_tile, loser_color, turn_panel, screen, timer, valid_moves, piece)
    #                     if game.is_game_over:
    #                         game.start_end_loop()
    #             elif event.type == TIMER_EVENT:
    #                 if timer.get_time() <= 0:
    #                     game.change_turn()
    #                     game.turn -= 1
    #                     if selected_tile:
    #                         selected_tile.unhighlight()
    #                         selected_tile = None
    #                     for tile in tiles:
    #                         tile.unhighlight()
    #                     turn_panel.update(screen, game.current_state)
    #                     timer.reset_timer()
    #                 else:
    #                     timer.update_timer()
    #     screen.fill(WHITE)
    #     for tile in tiles:
    #         tile.draw(screen)

    #     white_inventory.draw(screen)
    #     black_inventory.draw(screen)

    #     turn_panel.draw(screen, timer.get_time())
    #     pygame.time.Clock().tick(60)  # 60 frames per second for better experience
    #     pygame.display.flip()
    # End menu game loop
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
