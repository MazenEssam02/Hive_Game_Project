import pygame
import sys
from constant import WIDTH , HEIGHT , WHITE, RADIUS
from hex import draw_grid
#init pygame
pygame.init()

#set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello World")

#main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    #fill screen with white
    screen.fill(WHITE)
    
    #draw grid
    draw_grid(screen, rows=12, cols=12)
    #update the display
    pygame.display.flip()

#quit pygame

pygame.quit()
sys.exit()
