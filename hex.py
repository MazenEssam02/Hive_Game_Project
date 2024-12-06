import pygame
from constant import RADIUS, BLUE, HORIZONTAL_SPACING, VERTICAL_SPACING, GREY, DARK_BLUE
import math


class hex:
    def __init__(self, row, col, center, color, piece=None):
        self.position = (row, col)  # row + col % 2 = 0
        self.stroke = 1
        self.center = center  # in pixels
        self.points = []  # 6 points to draw the hexagon
        self.get_points(RADIUS, self.center)
        self.radius = RADIUS
        self.color = color
        self.prev_color = color
        if piece:
            self.pieces = [piece]
        else:
            self.pieces = []
        if row == 7 and col == 17:
            self.is_center_tile = True
        else:
            self.is_center_tile = False

    # draw one hexagon
    def draw(self, surface):
        pygame.draw.polygon(surface, self.color,
                            self.points, self.stroke)  # 1 for outline
        if self.has_pieces():
            self.pieces[-1].draw(surface, self.center)
            return

        # if self.is_center_tile:
        #     pygame.draw.polygon(surface, BLUE, self.points, 0)

    def get_points(self, radius, center):
        for i in range(6):
            angle = math.radians(60 * i - 30)
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            self.points.append((x, y))

    def add_piece(self, piece):
        self.pieces.append(piece)
        self.pieces[-1].update_pos(self.position)

    def remove_piece(self):
        self.pieces.pop(-1)

    def move_piece(self, new_tile):
        new_tile.add_piece(self.pieces[-1])
        self.remove_piece()

    def has_pieces(self):
        if len(self.pieces) > 0:
            return True
        else:
            return False

    def contains_point(self, surface, point):
        x, y = point
        return pygame.draw.polygon(surface, self.color, self.points, 0).collidepoint(x, y)

    def highlight(self):
        self.color = BLUE
        self.stroke = 2

    def unhighlight(self):
        self.color = self.prev_color
        self.stroke = 1

    def selected(self):
        self.color = DARK_BLUE
        self.stroke = 3

class Inventory_Tile(hex):

    def __init__(self,  center, radius, color, piece):
        super().__init__(-20, -20, center, color, piece)


def hex_neighbors(hex):
    # directions = [(0, -2), (0, 2), (-1, 1), (-1, -1), (1, -1), (1, 1)]
    directions = [(0, -2), (-1, -1),(-1, 1), (0, 2), (1, 1), (1, -1)]
    neighbors = []
    for d in directions:
        if (hex[0] + d[0] >= 0 and hex[0] + d[0] < 15 and hex[1] + d[1] >= 0 and hex[1] + d[1] < 36):
            neighbors.append(
                (hex[0] + d[0], hex[1] + d[1]))
    return neighbors


def draw_grid(surface, rows, cols):
    tiles = []
    for row in range(rows):
        for col in range(cols):
            # Calculate the center of each hexagon
            x = col * HORIZONTAL_SPACING + \
                (row % 2) * HORIZONTAL_SPACING / 2
            y = row * VERTICAL_SPACING
            # Offset to fit in the screen
            center = (x + RADIUS-4, y + RADIUS)
            if row % 2 == 0:
                col = col * 2
            else:
                col = col * 2 + 1
            # if row == 7 and col == 17:
            #     hexagon = Center_hex(row, col, center, BLUE)
            #     hexagon.draw_center(surface)

            # else:
            hexagon = hex(row, col, center, GREY)
            hexagon.draw(surface)
            tiles.append(hexagon)
    return tiles

def hex_distance(a, b):
    return (abs(a[0] - b[0]) + abs(a[0] + a[1] - b[0] - b[1]) + abs(a[1] - b[1])) // 2

def get_clicked_hex(surface, tiles, mouse_pos):
    for tile in tiles:
        if tile.contains_point(surface, mouse_pos):
            return tile
    return None

def generate_tile_dict(tiles):
    return {tile.position: tile for tile in tiles}
