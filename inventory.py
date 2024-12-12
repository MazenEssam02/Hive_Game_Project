import pygame
from Model import QueenBee, Grasshopper, Spider, Beetle, SoldierAnt
from hex import Inventory_Tile
from constant import WHITE, DARK_BLUE, WIDTH, HEIGHT,GREY


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
        inventory_height = 170
        self.col=0
        inner_left = left + 5
        inner_top = top + 5
        inner_width = inventory_width - 10
        inner_height = inventory_height - 5

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
            self.bg_color=WHITE
            self.row=-20
        else:
            self.color = 'BLACK'
            self.bg_color=GREY
            self.row=-10
        for i in range(0, 5):
            self.tile_rects.append(pygame.Rect(inner_left + i * stock_width
                                   + 2, inner_top + title_height + 2,
                                   stock_width - 4, stock_height - 4))

            if i == 0:
                tile_pos = (inner_left + i * stock_width + stock_width
                            / 2, inner_top + title_height
                            + stock_height / 2)
                self.tiles.append(Inventory_Tile(self.row,self.col,tile_pos,
                                  20, self.bg_color,
                                  piece=QueenBee(self.color)))
            if i == 1:
                self.row+=1
                for j in range(1, 3):
                    self.col+=1
                    tile_pos = (inner_left + i * stock_width
                                + stock_width / 2, inner_top
                                + title_height + j * stock_height / 3)
                    self.tiles.append(Inventory_Tile(self.row,self.col,tile_pos, 20, self.bg_color,
                                                     piece=Beetle(self.color)))
            if i == 2:
                self.row+=1
                for j in range(1, 3):
                    self.col+=1
                    tile_pos = (inner_left + i * stock_width
                                + stock_width / 2, inner_top
                                + title_height + j * stock_height / 3)
                    self.tiles.append(Inventory_Tile(self.row,self.col,tile_pos, 20, self.bg_color,
                                                     piece=Spider(self.color)))
            if i == 3:
                self.row+=1
                for j in [25, 67, 109]:
                    self.col+=1
                    tile_pos = (inner_left + i * stock_width
                                + stock_width / 2, inner_top
                                + title_height + j * stock_height / 135)
                    self.tiles.append(Inventory_Tile(self.row,self.col,tile_pos, 20, self.bg_color,
                                                     piece=Grasshopper(self.color)))
            if i == 4:
                self.row+=1
                for j in [25, 67, 109]:
                    self.col+=1
                    tile_pos = (inner_left + i * stock_width
                                + stock_width / 2, inner_top
                                + title_height + j * stock_height / 135)
                    self.tiles.append(Inventory_Tile(self.row,self.col,
                        tile_pos, 20, self.bg_color, piece=SoldierAnt(self.color)))
        for tile in self.tiles:
            tile.pieces[0].update_pos(tile.center)

        FONT = pygame.font.SysFont('Times New Norman', 24)
        if player == 0:
            self.font = FONT.render('Player 1 Inventory', True, WHITE)
        else:
            self.font = FONT.render('Player 2 Inventory', True, WHITE)
        self.title_rect = self.font.get_rect(center=(inner_left
                                                     + inner_width / 2, inner_top + title_height / 2))

    def draw(self, background):

        pygame.draw.rect(background, DARK_BLUE, self.back_panel)
        pygame.draw.rect(background, DARK_BLUE, self.inner_panel)
        pygame.draw.rect(background, DARK_BLUE, self.title_rect)
        for i in range(0, len(self.tile_rects)):
            pygame.draw.rect(background, self.bg_color, self.tile_rects[i])
        for tile in self.tiles:
            for piece in tile.pieces:
                piece.update_pos(tile.center)
                piece.draw(background, tile.center)
                tile.draw(background)
        background.blit(self.font, self.title_rect)
        return self.tiles
