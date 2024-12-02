import pygame
from constant import TIMER_EVENT , GAME_STATES

class state:
    def __init__(self , current_state):
        if current_state in GAME_STATES:
            self.current_state = current_state
        else:
            self.current_state = ''
    def change_turn(self):
        pygame.time.set_timer(TIMER_EVENT , 1000)
        if self.current_state == 'WHITE TURN' :
            self.current_state = 'BLACK TURN'
        elif self.current_state == 'BLACK TURN':
            self.current_state == 'WHITE TURN'
    def start_game(self):
        self.turn = 1
        self.current_state = 'WHITE TURN'
        #drigger event in Timer_event every 1sec
        pygame.time.set_timer(TIMER_EVENT , 1000)
    def get_turn(self):
        if self.current_state == 'WHITE TURN':
            return 'WHITE TURN'
        elif self.current_state == 'BLACK TURN':
            return 'BLACK TURN'
    
