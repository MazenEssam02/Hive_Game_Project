import pygame
from constant import TIMER_EVENT


class state:

    def __init__(self):
        self.running = True
        self.menu_loop = True
        self.main_loop = False
        self.end_loop = False
        self.opponent_menu = False
        self.difficulitiy_menu = False
        self.play_new_game = False
        self.selected_opponent = None
        self.selected_difficulty = None

    def start_end_loop(self):
        self.difficulitiy_menu = False
        self.menu_loop = False
        self.main_loop = False
        self.end_loop = True

    def start_difficulty_menu(self):
        self.menu_loop = False
        self.opponent_menu = False
        self.difficulitiy_menu = True

    def start_opponent_menu(self):
        self.menu_loop = False
        self.opponent_menu = True
        self.end_loop = False
        self.play_new_game = False
    def start_menu_loop(self):
        self.menu_loop = True
        self.main_loop = False
    def start_main_loop(self):
        self.opponent_menu = False
        self.difficulitiy_menu = False
        self.menu_loop = False
        self.play_new_game = False 
        self.main_loop = True
        self.start_game()
    def start_new_game(self):
        self.opponent_menu = False
        self.difficulitiy_menu = False
        self.menu_loop = False
        self.main_loop = False
        self.end_loop = False
        self.play_new_game = True 
    def quit(self):
        self.opponent_menu = False
        self.difficulitiy_menu = False
        self.running = False
        self.menu_loop = False
        self.main_loop = False
        self.end_loop = False

    def change_turn(self):
        # Increment the turn counter
        self.turn += 1
        # pygame.time.set_timer(TIMER_EVENT , 1000)
        if self.current_state == 'WHITE':
            self.current_state = 'BLACK'
        elif self.current_state == 'BLACK':
            self.current_state = 'WHITE'

    def start_game(self):
        self.current_state = 'WHITE'
        self.turn = 1  # Initialize the turn counter
        # drigger event in Timer_event every 1sec
        pygame.time.set_timer(TIMER_EVENT, 1000)

    def get_turn(self):
        return self.current_state

class TurnTimer():
    def __init__(self):
        self.turn_time = 180
        self.timer_event = TIMER_EVENT
        pygame.time.set_timer(self.timer_event, 1000)

    def update_timer(self):
        if self.turn_time > 0:
            self.turn_time -= 1

    def reset_timer(self):
        self.turn_time = 180

    def get_time(self):
        return self.turn_time
    
class GameState:
    def __init__(self):
        self.turn = 1
        self.current_state = 'WHITE'
        self.tiles = []
        self.tile_dict = {tile.position: tile for tile in self.tiles}
        self.selected_tile = None
        self.selected_piece = None
        self.selected_piece_moves = []
        self.history = []

    def make_move(self, piece, from_tile, to_tile):
        self.history.append({"piece": piece, "from_tile": from_tile, "to_tile": to_tile})
        piece.position = to_tile.position
        from_tile.pieces.remove(piece)
        to_tile.pieces.append(piece)
        self.turn += 1

    def undo_move(self):
        if not self.history:
            raise ValueError("No moves to undo!")
        last_move = self.history.pop()
        piece = last_move["piece"]
        from_tile = last_move["from_tile"]
        to_tile = last_move["to_tile"]
        piece.position = from_tile.position
        to_tile.pieces.remove(piece)
        from_tile.pieces.append(piece)
        self.turn -= 1