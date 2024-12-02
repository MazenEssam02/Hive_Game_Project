import pygame 
from Model import QueenBee, Grasshopper, Spider, Beetle, SoldierAnt
from hex import Inventory_Tile
from constant import WHITE, BLACK, WHITE, BLACK, PANEL, \
    WIDTH, HEIGHT


class Inventory_Frame:

    def __init__(
        self,
        pos,
        player,
        white=True,
        ):
        left = pos[0]
        top = HEIGHT - pos[1]

        inventory_width = WIDTH / 2
        inventory_height = 160

        inner_left = left + 5
        inner_top = top + 5
        inner_width = inventory_width - 10
        inner_height = inventory_height - 10

        self.back_panel = pygame.Rect(left, top, inventory_width,
                                  inventory_height)
        self.inner_panel = pygame.Rect(inner_left, inner_top, inner_width,
                                   inner_height)

        title_height = inner_height / 10
        stock_height = inner_height * (9 / 10)
        stock_width = inner_width / 5

        self.tile_rects = []
        self.tiles = []

        if white:
            self.color = 'WHITE'
        else:
            self.color = 'BLACK'
        for i in range(0, 5):
            self.tile_rects.append(pygame.Rect(inner_left + i * stock_width
                                   + 2, inner_top + title_height + 2,
                                   stock_width - 4, stock_height - 4))

            if i == 0:
                tile_pos = (inner_left + i * stock_width + stock_width
                            / 2, inner_top + title_height
                            + stock_height / 2)
                self.tiles.append(Inventory_Tile(tile_pos,
                                  20, self.color,
                                  piece=QueenBee(self.color)))
            if i == 1:
                for j in range(1, 3):
                    tile_pos = (inner_left + i * stock_width
                                + stock_width / 2, inner_top
                                + title_height + j * stock_height / 3)
                    self.tiles.append(Inventory_Tile(tile_pos, 20, self.color,
                            piece=Beetle(self.color)))
            if i == 2:
                for j in range(1, 3):
                    tile_pos = (inner_left + i * stock_width
                                + stock_width / 2, inner_top
                                + title_height + j * stock_height / 3)
                    self.tiles.append(Inventory_Tile(tile_pos, 20, self.color,
                            piece=Spider(self.color)))
            if i == 3:
                for j in [25, 67, 109]:
                    tile_pos = (inner_left + i * stock_width
                                + stock_width / 2, inner_top
                                + title_height + j * stock_height / 135)
                    self.tiles.append(Inventory_Tile(tile_pos, 20, self.color,
                            piece=Grasshopper(self.color)))
            if i == 4:
                for j in [25, 67, 109]:
                    tile_pos = (inner_left + i * stock_width
                                + stock_width / 2, inner_top
                                + title_height + j * stock_height / 135)
                    self.tiles.append(Inventory_Tile(tile_pos, 20, self.color, piece=SoldierAnt(self.color)))
        for tile in self.tiles:
            for piece in tile.pieces:
                piece.update_pos(tile.center)
                

        FONT = pygame.font.SysFont('Times New Norman', 24)
        if player == 0:
            self.font = FONT.render('Player 1 Inventory', True, WHITE)
        else:
            self.font = FONT.render('Player 2 Inventory', True, WHITE)
        self.title_rect = self.font.get_rect(center=(inner_left
                + inner_width / 2, inner_top + title_height / 2))

    def draw(self, background):

        pygame.draw.rect(background, BLACK, self.back_panel)
        pygame.draw.rect(background, PANEL, self.inner_panel)
        pygame.draw.rect(background, PANEL, self.title_rect)
        for i in range(0, len(self.tile_rects)):
            pygame.draw.rect(background, self.color, self.tile_rects[i])
        for tile in self.tiles:
            for piece in tile.pieces:
                piece.update_pos(tile.center)
                piece.draw(background, tile.center)
        background.blit(self.font, self.title_rect)
        