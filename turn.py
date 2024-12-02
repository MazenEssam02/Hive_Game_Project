import pygame
from constant import PANEL, WHITE , BLACK ,BACKGROUND
# class turn:
#     def __init__(self, pos , player):
#         self.width = 100
#         self.height = 50
#         self.pos = pos
#         self.player = player
#         self.panel = pygame.Rect(self.pos[0] , self.pos[1] , self.width , self.height)
#     def draw(self, surf):
#         if self.player == 'White':
#             cc = WHITE
#         else:
#             cc = BLACK
#         pygame.draw.rect(surf, PANEL , self.panel , 0)
#         pygame.draw.circle(surf , cc , (self.pos[0]+self.width // 2 , self.pos[1] + self.height // 2) , 15 , 3)
#     def my_turn(self, surf):
#         pygame.draw.circle(surf , PANEL , (self.pos[0]+self.width // 2 , self.pos[1] + self.height // 2) , 15 , 0)

class turn_terminal:
    def __init__(self , pos):
        self.width = 300
        self.height = 50
        self.pos = pos
        self.panel = pygame.Rect(self.pos[0] , self.pos[1] , self.width , self.height)
        self.inner_panel = pygame.Rect(self.pos[0] + 50 , self.pos[1] + 5 , 200 , 40)
    def draw(self, surf, turn):
        pygame.draw.rect(surf, BACKGROUND , self.panel , 0)
        pygame.draw.rect(surf, WHITE , self.inner_panel, 0)
        pygame.draw.circle(surf , WHITE , (self.pos[0]+ 25 , self.pos[1] + 25) , 15 , 3)
        pygame.draw.circle(surf , WHITE , (self.pos[0] + 275, self.pos[1] + 25) , 15 , 3)
        FONT = pygame.font.SysFont('Times New Norman', 24)
        if turn == 'WHITE TURN':
            self.font = FONT.render('White Turn' , True, BLACK)
            pygame.draw.circle(surf , WHITE , (self.pos[0]+ 25 , self.pos[1] + 25) , 15 , 0)
        else:
            self.font = FONT.render('Black Turn', True , BLACK)
            pygame.draw.circle(surf , BLACK , (self.pos[0] + 275, self.pos[1] + 25) , 15 , 0)
        center = (self.pos[0] + self.width / 2, self.pos[1] + self.height / 2)
        self.turn_title = self.font.get_rect(center=(center))
        surf.blit(self.font, self.turn_title)
    def update(self, surf, turn):
        self.draw(surf, turn)
