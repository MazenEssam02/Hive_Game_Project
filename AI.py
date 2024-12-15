from Controller import get_all_valid_moves_for_color, hex_neighbors
import hex
class AI:
    def __init__(self, color,difficulty):
        self.color = color
        self.difficulty = difficulty
        self.piece_values = {
            "Queen Bee": 1,
            "Beetle": 3,  # Important for attacking and covering
            "Spider":5 ,  # Good for pinning pieces
            "Soldier Ant": 10,  # Excellent mobility for surrounding
            "Grasshopper": 7,
        }


    def move_piece(self,piece, old_position, new_position, all_tile_dict):
        all_tile_dict[old_position].remove_piece()
        all_tile_dict[new_position].add_piece(piece)

        if piece.piece_type == "Queen Bee":
                if piece.color == "BLACK":
                    hex.black_queen_position = new_position
                elif piece.color == "WHITE":
                    hex.white_queen_position = new_position

    def undo_move(self,piece, old_position, new_position, all_tile_dict):
        all_tile_dict[new_position].remove_piece()
        all_tile_dict[old_position].add_piece(piece)

        if piece.piece_type == "Queen Bee":
                if piece.color == "BLACK":
                    hex.black_queen_position = old_position
                elif piece.color == "WHITE":
                    hex.white_queen_position = old_position

    def count_queenbee_black_surronded(self,tiles_dict):
        black_queenbee = 0
        queen_bee_position = None

        # Find the position of the black queen bee
        for tile in tiles_dict.values():
            if tile.has_pieces():
                for piece in tile.pieces:
                    if piece.piece_type == "Queen Bee" and piece.color == "BLACK":
                        queen_bee_position = tile.position
                        break
                if queen_bee_position:
                    break

        if not queen_bee_position:
            return 0  # No black queen bee found

        # Count the number of surrounding tiles that are occupied
        for neighbor_pos in hex_neighbors(queen_bee_position):
            neighbor_tile = tiles_dict.get(neighbor_pos)
            if neighbor_tile and neighbor_tile.has_pieces():
                black_queenbee += 1

        return black_queenbee
    def count_queenbee_white_surronded(self,tiles_dict):
        white_queenbee = 0
        queen_bee_position = None

        # Find the position of the white queen bee
        for tile in tiles_dict.values():
            if tile.has_pieces():
                for piece in tile.pieces:
                    if piece.piece_type == "Queen Bee" and piece.color == "WHITE":
                        queen_bee_position = tile.position
                        break
                if queen_bee_position:
                    break

        if not queen_bee_position:
            return 0  # No black queen bee found

        # Count the number of surrounding tiles that are occupied
        for neighbor_pos in hex_neighbors(queen_bee_position):
            neighbor_tile = tiles_dict.get(neighbor_pos)
            if neighbor_tile and neighbor_tile.has_pieces():
                white_queenbee += 1

        return white_queenbee

    def count_pieces(self,tile_dict, color):
        count = 0
        for tile in tile_dict.values():
            for piece in tile.pieces:
                if piece.color == color:
                    count += 1
        return count

    def count_valid_moves(self,game, tiles, tile_dict, all_tiles,color):
        valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict,all_tiles,color)
        move_count = sum(len(moves) for moves in valid_moves.values())
        return move_count

    # def piece_value(self,piece):
    #     if piece.piece_type == "Queen Bee":
    #         return 1
    #     elif piece.piece_type == "Beetle":
    #         return 3
    #     elif piece.piece_type == "Soldier Ant":
    #         return 10
    #     elif piece.piece_type == "Grasshopper":
    #         return 7
    #     elif piece.piece_type == "Spider":
    #         return 5
    #     return 0

    def evaluate_pieces(self,tile_dict, color):
        value = 0
        for tile in tile_dict.values():
            for piece in tile.pieces:
                if piece.color == color:
                    value += self.piece_values[piece.piece_type]
        return value

    def get_queen_position(self,tiles, color):
        for tile in tiles:
            if tile.has_pieces():
                for piece in tile.pieces:
                    if piece.piece_type == "Queen Bee" and piece.color == color:
                        return tile.position
        return None

    def get_pieces_positions(self,tile_dict, color):
        return [position for position, piece in tile_dict.items() if piece.color == color]

    def distance(self,pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)

    def scoreBoard(self,game, tiles, tile_dict, all_tiles, all_tile_dict):
        black_surrounded = self.count_queenbee_black_surronded(tile_dict)
        white_surrounded = self.count_queenbee_white_surronded(tile_dict)

        black_piece_count = self.count_pieces(tile_dict, "BLACK")
        white_piece_count = self.count_pieces(tile_dict, "WHITE")

        black_move_count = self.count_valid_moves(game, tiles, tile_dict, all_tiles, "BLACK")
        white_move_count = self.count_valid_moves(game, tiles, tile_dict, all_tiles, "WHITE")

        black_piece_value = self.evaluate_pieces(tile_dict, "BLACK")
        white_piece_value = self.evaluate_pieces(tile_dict, "WHITE")

        # New heuristic: distance to white queen
        white_queen_position = self.get_queen_position(tiles, "WHITE")
        black_pieces_positions = self.get_pieces_positions(tile_dict, "BLACK")
        distance_to_white_queen = sum(self.distance(pos, white_queen_position) for pos in black_pieces_positions)

        # Heuristic weights
        queen_surround_weight = 100  # Increased weight for surrounding the queen
        piece_count_weight = 1
        move_count_weight = 1
        piece_value_weight = 2
        attack_white_queen_weight = -10  # Negative weight to minimize distance to white queen

        score = (queen_surround_weight * (-black_surrounded + white_surrounded) +
                 piece_count_weight * (black_piece_count - white_piece_count) +
                 move_count_weight * (black_move_count - white_move_count) +
                 piece_value_weight * (black_piece_value - white_piece_value) +
                 attack_white_queen_weight * distance_to_white_queen)

        return score

    def board_value(self,game,tiles,tile_dict,all_tiles,all_tile_dict):
        result = self.scoreBoard(game,tiles,tile_dict,all_tiles,all_tile_dict)
        if game.current_state == "BLACK":
            return result * -1
        return result

    def minimax(self,game, tiles, tile_dict,all_tiles, all_tile_dict, depth, maximizing_player):
        if depth == 0 :
            return None,self.board_value(game, tiles, tile_dict,all_tiles,all_tile_dict)

        best_move=None

        if maximizing_player:
            valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict, all_tiles,"WHITE")
            best_value = -1000
            for (piece, position), moves in valid_moves.items():
                for move in moves:
                    self.move_piece(piece, position, move, all_tile_dict)
                    _,value = self.minimax(game, tiles, tile_dict,all_tiles,all_tile_dict, depth - 1, False)
                    self.undo_move(piece, position, move, all_tile_dict) # Revert move
                    if value > best_value:
                        best_value = value
                        best_move=(piece,position,move)
            return best_move,best_value
        else:
            valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict, all_tiles,"BLACK")
            best_value = 1000
            for (piece, position), moves in valid_moves.items():
                for move in moves:
                    self.move_piece(piece, position, move, all_tile_dict)
                    _,value = self.minimax(game, tiles, tile_dict, all_tiles,all_tile_dict,depth - 1, True)
                    self.undo_move(piece, position, move, all_tile_dict)  # Revert move
                    if value < best_value:
                        best_value = value
                        best_move=(piece,position,move)

            return best_move,best_value

    def minimax_with_pruning(self,game, tiles, tile_dict,all_tiles, all_tile_dict, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.is_game_over:
            return self.board_value(game, tiles, tile_dict,all_tiles,all_tile_dict)

        if maximizing_player:
            valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict,all_tiles,"WHITE")
            best_value = -1000
            for (piece, position), moves in valid_moves.items():
                for move in moves:
                    self.move_piece(piece, position, move, all_tile_dict)
                    value = self.minimax_with_pruning(game, tiles, tile_dict, all_tiles, all_tile_dict, depth - 1, alpha, beta, False)
                    self.undo_move(piece, position, move, all_tile_dict)  # Revert move
                    best_value = max(best_value, value)
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        print(f"beta cut off: ({alpha}) , {beta})")
                        break  # Beta cut-off
            return best_value
        else:
            valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict,all_tiles,"BLACK")
            best_value = 1000
            for (piece, position), moves in valid_moves.items():
                for move in moves:
                    self.move_piece(piece, position, move, all_tile_dict)
                    value = self.minimax_with_pruning(game, tiles, tile_dict,all_tiles, all_tile_dict, depth - 1, alpha, beta, True)
                    self.undo_move(piece, position, move, all_tile_dict)  # Revert move
                    best_value = min(best_value, value)
                    beta = min(beta, value)
                    if beta <= alpha:
                        print(f"alpha cut off: ({alpha}) , {beta})")
                        break  # Alpha cut-off
            return best_value

    def ai_move(self,game, tiles, tile_dict, all_tiles, all_tile_dict,depth=1):
        piece=None
        position = None
        move = None
        if(self.color == "BLACK"):
             (piece, position, move), value = self.minimax(game, tiles, tile_dict, all_tiles, all_tile_dict, depth, False)
        elif(self.color == "WHITE"):
            (piece, position, move), value = self.minimax(game, tiles, tile_dict, all_tiles, all_tile_dict, depth, True)
        best_move = (piece,all_tile_dict[position], tile_dict[move])
        return best_move