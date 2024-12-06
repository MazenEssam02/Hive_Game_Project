import pygame
from constant import WHITE , BLACK ,DARK_BLUE
class turn_terminal:
    def __init__(self , pos , turn):
        self.width = 300
        self.height = 50
        self.pos = pos
        self.panel = pygame.Rect(self.pos[0] , self.pos[1] , self.width , self.height)
        self.inner_panel = pygame.Rect(self.pos[0] + 50 , self.pos[1] + 5 , 200 , 40)
        self.game_turn = turn 
    def draw(self, surf, remaining_time=180):
        pygame.draw.rect(surf, DARK_BLUE , self.panel , 0)
        pygame.draw.rect(surf, WHITE , self.inner_panel, 0)
        pygame.draw.circle(surf , WHITE , (self.pos[0]+ 25 , self.pos[1] + 25) , 15 , 2)
        pygame.draw.circle(surf , BLACK , (self.pos[0] + 275, self.pos[1] + 25) , 15 , 2)
        FONT = pygame.font.SysFont('Times New Norman', 24)
        if self.game_turn == 'WHITE':
            self.font = FONT.render('White Turn' , True, BLACK)
            pygame.draw.circle(surf , WHITE , (self.pos[0]+ 25 , self.pos[1] + 25) , 15 , 0)
        else:
            self.font = FONT.render('Black Turn', True , BLACK)
            pygame.draw.circle(surf , BLACK , (self.pos[0] + 275, self.pos[1] + 25) , 15 , 0)
        # Turn Text
        center = (self.pos[0] + self.width / 2, self.pos[1] + self.height / 2 - 10)
        self.turn_title = self.font.get_rect(center=(center))
        # Time Text
        self.time_text = FONT.render(f"{remaining_time // 60}:{remaining_time % 60:02d}", True, BLACK)
        self.time_container = self.time_text.get_rect(center=(center[0] , center[1] + 20 )) 
        surf.blit(self.font, self.turn_title)
        surf.blit(self.time_text, self.time_container)
    def update(self, surf, turn, remaining_time=180):
        self.game_turn = turn
        self.draw(surf , remaining_time)
