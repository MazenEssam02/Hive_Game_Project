import pygame
from constant import TIMER_EVENT

class state:
    def __init__(self ):
        self.start_game()
    def change_turn(self):
        # pygame.time.set_timer(TIMER_EVENT , 1000)
        if self.current_state == 'WHITE TURN' :
            self.current_state = 'BLACK TURN'
        elif self.current_state == 'BLACK TURN':
            self.current_state = 'WHITE TURN'
    def start_game(self):
        self.current_state = 'WHITE TURN'
        #drigger event in Timer_event every 1sec
        pygame.time.set_timer(TIMER_EVENT , 1000)
    def get_turn(self):
        if self.current_state == 'WHITE TURN':
            return 'WHITE TURN'
        elif self.current_state == 'BLACK TURN':
            return 'BLACK TURN'
    
class TurnTimer():
    def __init__(self):
        self.turn_time = 180
        self.timer_event = TIMER_EVENT
        pygame.time.set_timer(self.timer_event , 1000)
    def update_timer(self):
        if self.turn_time > 0:
            self.turn_time -= 1
    def reset_timer(self):
        self.turn_time = 180
    def get_time(self):
        return self.turn_time