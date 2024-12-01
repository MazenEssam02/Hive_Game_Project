import pygame
from constant import WIDTH_HEX, HEIGHT_HEX, RADIUS, BLUE, HORIZONTAL_SPACING, VERTICAL_SPACING
import math


class hex:
    def __init__(self, row, col, center, color, piece=None):
        self.position = (row, col)  # row + col % 2 = 0
        self.center = center  # in pixels
        self.points = []  # 6 points to draw the hexagon
        self.get_points(RADIUS, self.center)
        self.radius = RADIUS
        self.color = color
        if piece:
            self.piece = [piece]
        else:
            self.piece = []

    # draw one hexagon
    def draw(self, surface):
        pygame.draw.polygon(surface, BLUE, self.points, 1)  # 1 for outline

    # get the points of hexagon from https://www.redblobgames.com/grids/hexagons/
    def get_points(self, radius, center):
        for i in range(6):
            angle = math.radians(60 * i - 30)
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            self.points.append((x, y))


def draw_grid(surface, rows, cols):
    tiles = []
    for row in range(rows):
        for col in range(cols):
            # Calculate the center of each hexagon
            x = col * HORIZONTAL_SPACING + (row % 2) * HORIZONTAL_SPACING / 2
            y = row * VERTICAL_SPACING
            center = (x+RADIUS, y + RADIUS)  # Offset to fit in the screen
            if row % 2 == 0:
                col = col * 2
            else:  
                col = col * 2 + 1
            hexagon = hex(row, col, center, BLUE)
            tiles.append(hexagon)
            hexagon.draw(surface)
    return tiles

def hex_distance(a, b):
    return (abs(a[0] - b[0]) + abs(a[0] + a[1] - b[0] - b[1]) + abs(a[1] - b[1])) // 2

def hex_neighbors(hex):
    directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
    return [(hex[0] + d[0], hex[1] + d[1]) for d in directions]
