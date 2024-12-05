from hex import hex_neighbors
import pygame
from constant import RADIUS
from Controller import place_piece, is_piece_on_board, can_slide_out


class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color
        self.position = None

    def __repr__(self):
        return f"{self.color} {self.piece_type}"

    def update_pos(self, pos):
        self.position = pos


class QueenBee(Piece):
    def __init__(self, color):
        super().__init__("Queen Bee", color)

    def draw(self, surface, center):
        image = \
            pygame.image.load(f'assets/{type(self).__name__}_{self.color}.png')
        size = int(2*RADIUS)  # Scale the asset to fit inside the hex
        asset = pygame.transform.scale(image, (size, size))
        (x, y) = center
        pos = (x - RADIUS, y - RADIUS)
        surface.blit(asset, pos)

    def valid_moves(self, tiles):
        # Queen Bee can move one space in any direction
        valid_moves = []
        if is_piece_on_board(self, tiles):
            # The piece is on the board, check for neighboring tiles
            neighbors = hex_neighbors(self.position)
            free_spaces = can_slide_out(neighbors, tiles)
            if free_spaces:
                # Check if the queen moves adjacent to neighboring pieces 
                for free_space in free_spaces:
                    for neighbor_pos in neighbors:
                        neighbor_tile = next((t for t in tiles if t.position == neighbor_pos), None)
                        if neighbor_tile.has_pieces() and free_space in hex_neighbors(neighbor_pos):
                            valid_moves.append(free_space)
                            break
        else:
            # The piece is in the inventory, check for tiles already on the board
            valid_moves = place_piece(self, tiles)

        return valid_moves


class Beetle(Piece):
    def __init__(self, color):
        super().__init__("Beetle", color)

    def draw(self, surface, center):
        image = \
            pygame.image.load(f'assets/{type(self).__name__}_{self.color}.png')
        size = int(2*RADIUS)  # Scale the asset to fit inside the hex
        asset = pygame.transform.scale(image, (size, size))
        (x, y) = center
        pos = (x - RADIUS, y - RADIUS)
        surface.blit(asset, pos)

    # Beetle can move one space in any direction, including on top of other pieces
    def valid_moves(self, tiles):
        valid_moves = []
        if is_piece_on_board(self, tiles):
            # Check if the beetle is on top of the hive
            current_tile = next((t for t in tiles if t.position == self.position), None)
            if current_tile.pieces[0] == self:
                # The piece is on the board, check for neighboring tiles
                neighbors = hex_neighbors(self.position)
                free_spaces = can_slide_out(neighbors, tiles)
                if free_spaces:
                    # Check if the beetle moves adjacent to neighboring pieces 
                    for free_space in free_spaces:
                        for neighbor_pos in neighbors:
                            neighbor_tile = next((t for t in tiles if t.position == neighbor_pos), None)
                            if neighbor_tile.has_pieces() and free_space in hex_neighbors(neighbor_pos):
                                valid_moves.append(free_space)
                                break
                # Check if the beetle can move on top of other pieces
                for neighbor in neighbors:
                    for tile in tiles:
                        if neighbor == tile.position and tile.has_pieces():
                            valid_moves.append(neighbor)
            # The beetle is on top of the hive
            else:
                neighbors = hex_neighbors(self.position)
                for neighbor in neighbors:
                    valid_moves.append(neighbor)
            
        else:
            # The piece is in the inventory, check for tiles already on the board
            valid_moves = place_piece(self, tiles)

        return valid_moves

class Grasshopper(Piece):
    def __init__(self, color):
        super().__init__("Grasshopper", color)

    def draw(self, surface, center):
        image = \
            pygame.image.load(f'assets/{type(self).__name__}_{self.color}.png')
        size = int(2*RADIUS)  # Scale the asset to fit inside the hex
        asset = pygame.transform.scale(image, (size, size))
        (x, y) = center
        pos = (x - RADIUS, y - RADIUS)
        surface.blit(asset, pos)

    # Grasshopper jumps over pieces in a straight line
    def valid_moves(self, tiles):
        valid_moves = []
        if is_piece_on_board(self, tiles):
            # The piece is on the board, check for neighboring tiles
            directions = [(0, -2), (0, 2), (-1, 1), (-1, -1), (1, -1), (1, 1)]
            for direction in directions:
                current_pos = self.position
                # Move to the next position in the current direction
                current_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                current_tile = next((t for t in tiles if t.position == current_pos), None)
                # Check if it will jump over an adjacent piece
                if current_tile and current_tile.has_pieces():
                    # Continue moving in the same direction until an empty tile is found
                    while True:
                        # Check if the tile is empty and add it to the valid moves
                        if not current_tile.has_pieces():
                            valid_moves.append(current_pos)
                            break
                        # Move to the next position in the current direction
                        current_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                        current_tile = next((t for t in tiles if t.position == current_pos), None)
        else:
            # The piece is in the inventory, check for tiles already on the board
            valid_moves = place_piece(self, tiles)

        return valid_moves

class Spider(Piece):
    def __init__(self, color):
        super().__init__("Spider", color)

    def draw(self, surface, center):
        image = \
            pygame.image.load(f'assets/{type(self).__name__}_{self.color}.png')
        size = int(2*RADIUS)  # Scale the asset to fit inside the hex
        asset = pygame.transform.scale(image, (size, size))
        (x, y) = center
        pos = (x - RADIUS, y - RADIUS)
        surface.blit(asset, pos)

    def valid_moves(self, tiles):
        # Queen Bee can move one space in any direction
        valid_moves = []
        if is_piece_on_board(self, tiles):
            # The piece is on the board, check for neighboring tiles
            neighbors = hex_neighbors(self.position)
            for neighbor in neighbors:
                for tile in tiles:
                    if neighbor == tile.position and not tile.has_pieces():
                        valid_moves.append(neighbor)
        else:
            # The piece is in the inventory, check for tiles already on the board
            valid_moves = place_piece(self, tiles)

        return valid_moves

        # # Spider moves exactly three spaces
        # def dfs(position, depth, visited):
        #     if depth == 3:
        #         return [position]
        #     moves = []
        #     for neighbor in hex_neighbors(position):
        #         if neighbor not in visited and neighbor in board.board:
        #             # Check if the neighbor is adjacent to the hive
        #             if any(adj in board.board for adj in hex_neighbors(neighbor)):
        #                 visited.add(neighbor)
        #                 moves.extend(dfs(neighbor, depth + 1, visited))
        #                 visited.remove(neighbor)
        #     return moves

        # visited = {self.position}
        # return dfs(self.position, 0, visited)


class SoldierAnt(Piece):
    def __init__(self, color):
        super().__init__("Soldier Ant", color)

    def draw(self, surface, center):
        image = \
            pygame.image.load(f'assets/{type(self).__name__}_{self.color}.png')
        size = int(2*RADIUS)  # Scale the asset to fit inside the hex
        asset = pygame.transform.scale(image, (size, size))
        (x, y) = center
        # Offset to fit in the center of the hex
        pos = (x - RADIUS, y - RADIUS)
        surface.blit(asset, pos)

    def valid_moves(self, tiles):
        # Queen Bee can move one space in any direction
        valid_moves = []
        if is_piece_on_board(self, tiles):
            # The piece is on the board, check for neighboring tiles
            neighbors = hex_neighbors(self.position)
            for neighbor in neighbors:
                for tile in tiles:
                    if neighbor == tile.position and not tile.has_pieces():
                        valid_moves.append(neighbor)
        else:
            # The piece is in the inventory, check for tiles already on the board
            valid_moves = place_piece(self, tiles)

        return valid_moves

        # # Soldier Ant can move to any position around the hive
        # def bfs(start):
        #     queue = [start]
        #     visited = {start}
        #     moves = []
        #     while queue:
        #         position = queue.pop(0)
        #         for neighbor in hex_neighbors(position):
        #             if neighbor not in visited and neighbor not in board.board:
        #                 # Check if the neighbor is adjacent to the hive
        #                 if any(adj in board.board for adj in hex_neighbors(neighbor)):
        #                     visited.add(neighbor)
        #                     queue.append(neighbor)
        #                     moves.append(neighbor)
        #     return moves

        # return bfs(self.position)
