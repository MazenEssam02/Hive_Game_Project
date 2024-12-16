from Controller import get_all_valid_moves_for_color, is_queen_surrounded
import hex
import time


class AI:
    def __init__(self, color, difficulty):
        self.color = color
        self.difficulty = difficulty
        self.time_limit = 20
        self.piece_values = {
            "Queen Bee": 1000,
            "Beetle": 80,  # Important for attacking and covering
            "Spider": 40,  # Good for pinning pieces
            "Soldier Ant": 60,  # Excellent mobility for surrounding
            "Grasshopper": 30,
        }

    def move_piece(self, piece, old_position, new_position, all_tile_dict):
        all_tile_dict[old_position].remove_piece()
        all_tile_dict[new_position].add_piece(piece)

        if piece.piece_type == "Queen Bee":
            if piece.color == "BLACK":
                hex.black_queen_position = new_position
            elif piece.color == "WHITE":
                hex.white_queen_position = new_position

    def undo_move(self, piece, old_position, new_position, all_tile_dict):
        all_tile_dict[new_position].remove_piece()
        all_tile_dict[old_position].add_piece(piece)

        if piece.piece_type == "Queen Bee":
            if piece.color == "BLACK":
                hex.black_queen_position = old_position
            elif piece.color == "WHITE":
                hex.white_queen_position = old_position

    def count_pieces(self, tile_dict, color):
        count = 0
        for tile in tile_dict.values():
            for piece in tile.pieces:
                if piece.color == color:
                    count += 1
        return count

    def count_valid_moves(self, game, tiles, tile_dict, all_tiles, color):
        valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict, all_tiles, color)
        move_count = sum(len(moves) for moves in valid_moves.values())
        return move_count

    def evaluate_pieces(self, tile_dict, color):
        value = 0
        for tile in tile_dict.values():
            for piece in tile.pieces:
                if piece.color == color:
                    value += self.piece_values[piece.piece_type]
        return value

    def get_queen_position(self, tiles, color):
        for tile in tiles:
            if tile.has_pieces():
                for piece in tile.pieces:
                    if piece.piece_type == "Queen Bee" and piece.color == color:
                        return tile.position
        return None

    def get_pieces_positions(self, tile_dict, color):
        return [position for position, piece in tile_dict.items() if piece.color == color]

    def distance(self, queen, tile):
        q1, r1 = queen
        q2, r2 = tile
        return (abs(q1 - q2) + abs(r1 - r2) + abs(-q1 - r1 + q2 + r2)) // 2

    def score_board(self, game, tiles, tile_dict, all_tiles, all_tile_dict,color):
        opposing_color = "WHITE" if color == "BLACK" else "BLACK"
        score = 0
        # categorizing pieces into friendly and opposing pieces
        friendly_pieces = []
        opposing_pieces = []
        for tile in tiles:
            if tile.has_pieces():
                for piece in tile.pieces:
                    if piece.color == color:
                        friendly_pieces.append(tile.position)
                        score += self.piece_values[piece.piece_type]
                    else:
                        opposing_pieces.append(tile.position)
                        score -= self.piece_values[piece.piece_type]

        # game ending conditions
        queen_surrounded = is_queen_surrounded(color, tile_dict)
        white_surrounded = queen_surrounded[1]
        black_surrounded = queen_surrounded[2]
        total_surrounded = white_surrounded + black_surrounded
        opposing_queen_surrounded = is_queen_surrounded(opposing_color, tile_dict)
        white_surrounding_enemy = opposing_queen_surrounded[1]
        black_surrounding_enemy = opposing_queen_surrounded[2]
        total_surrounding_enemy = white_surrounding_enemy + black_surrounding_enemy

        if queen_surrounded[0] == color:
            return float('-inf')
        elif queen_surrounded[0] == opposing_color:
            return float('inf')

        # early game development
        if game.turn <= 10:
            score += len(friendly_pieces) * 1000
            if game.turn == game.turn - 1:
                score -= len(opposing_pieces) * 1000
            print(f"Early game score: {score}")
        
        # queen safety
        queen_position = self.get_queen_position(tiles, color)
        opposing_queen_position = self.get_queen_position(tiles, opposing_color)
        if queen_position is not None:
            opposing_queen_position_neighbors = hex_neighbors(opposing_queen_position)
        if opposing_queen_position is not None:
            queen_position_neighbors = hex_neighbors(queen_position)

        # check if the queen is surrounded by friendly pieces (have same color)
        friendly_surr = 0
        enemy_surr = 0
        for neighbor in queen_position_neighbors:
            if neighbor in friendly_pieces:
                friendly_surr += 1
            elif neighbor in opposing_pieces:
                enemy_surr += 1
        
        if total_surrounded <= 1:
            score -= 200 # exposed
        elif total_surrounded == 2:
            score += 50 # good mobility
        elif total_surrounded == 3:
            score += friendly_surr * 40 # reward friendly protection
        elif total_surrounded >= 4:
            score -= 150*(total_surrounded-3) # punish for being surrounded
        print(f"surrounding score: {score}")

        # surrounding enemy queen
        score += total_surrounding_enemy * 2000 # reward for surrounding enemy queen

        friendly_move_count = self.count_valid_moves(game, tiles, tile_dict, all_tiles, color)
        opposing_move_count = self.count_valid_moves(game, tiles, tile_dict, all_tiles, opposing_color)

        friendly_pieces_value = self.evaluate_pieces(tile_dict, color)
        opposing_pieces_value = self.evaluate_pieces(tile_dict, opposing_color)

        # Heuristic weights
        move_count_weight = 1
        piece_value_weight = 2

        score += (move_count_weight * (friendly_move_count - opposing_move_count) +
                  piece_value_weight * (friendly_pieces_value - opposing_pieces_value)
                )

        return score

    def board_value(self, game, tiles, tile_dict, all_tiles, all_tile_dict,color):
        result = self.score_board(game, tiles, tile_dict, all_tiles, all_tile_dict,color)
        if game.current_state == "BLACK":
            return result * -1
        return result

    def minimax(self, game, tiles, tile_dict, all_tiles, all_tile_dict, depth, maximizing_player, start_time):
        if maximizing_player:
            color = "WHITE"
        else:
            color = "BLACK"
        if depth == 0 or time.time()-start_time >self.time_limit:
            return None, self.board_value(game, tiles, tile_dict, all_tiles, all_tile_dict,color)

        best_move = None
        place_piece = False

        if maximizing_player:
            valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict, all_tiles, "WHITE")
            best_value = float("-inf")
            for (piece, position), moves in valid_moves.items():
                if position[0] in range(-20, 0) and not place_piece:
                    place_piece = True
                    for move in moves:
                        self.move_piece(piece, position, move, all_tile_dict)
                        _, value = self.minimax(game, tiles, tile_dict, all_tiles, all_tile_dict, depth - 1, False,start_time)
                        self.undo_move(piece, position, move, all_tile_dict)  # Revert move
                        place_value = value - self.piece_values[piece.piece_type]  # General value for placing piece
                elif position[0] in range(-20, 0) and place_piece:
                    value = place_value + self.piece_values[piece.piece_type]
                else:
                    for move in moves:
                        self.move_piece(piece, position, move, all_tile_dict)
                        _, value = self.minimax(game, tiles, tile_dict, all_tiles, all_tile_dict, depth - 1, False, start_time)
                        self.undo_move(piece, position, move, all_tile_dict)
                if value > best_value or value == best_value:
                    best_value = value
                    best_move = (piece, position, move)

            return best_move, best_value
        else:
            valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict, all_tiles, "BLACK")
            best_value = float("inf")
            for (piece, position), moves in valid_moves.items():
                if position[0] in range(-20, 0) and not place_piece:
                    place_piece = True
                    for move in moves:
                        self.move_piece(piece, position, move, all_tile_dict)
                        _, value = self.minimax(game, tiles, tile_dict, all_tiles, all_tile_dict, depth - 1, True, start_time)
                        self.undo_move(piece, position, move, all_tile_dict)  # Revert move
                        place_value = value + self.piece_values[piece.piece_type]  # General value for placing piece
                elif position[0] in range(-20, 0) and place_piece:
                    value = place_value - self.piece_values[piece.piece_type]
                else:
                    for move in moves:
                        self.move_piece(piece, position, move, all_tile_dict)
                        _, value = self.minimax(game, tiles, tile_dict, all_tiles, all_tile_dict, depth - 1, False, start_time)
                        self.undo_move(piece, position, move, all_tile_dict)
                if value < best_value or value == best_value:
                    best_value = value
                    best_move = (piece, position, move)

            return best_move, best_value
            
    def minimax_with_pruning(self, game, tiles, tile_dict, all_tiles, all_tile_dict, depth,alpha,beta, maximizing_player , start_time):
        if maximizing_player:
            color = "WHITE"
        else:
            color = "BLACK"
        if depth == 0 or time.time()-start_time >self.time_limit:
            return None, self.board_value(game, tiles, tile_dict, all_tiles, all_tile_dict,color)

        best_move = None
        place_piece = False

        if maximizing_player:
            valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict, all_tiles, "WHITE")
            best_value = float("-inf")
            for (piece, position), moves in valid_moves.items():
                if position[0] in range (-20, 0) and not place_piece:
                    place_piece = True
                    for move in moves:
                        self.move_piece(piece, position, move, all_tile_dict)
                        _, value = self.minimax_with_pruning(game, tiles, tile_dict, all_tiles, all_tile_dict, depth - 1, alpha,beta,False , start_time)
                        self.undo_move(piece, position, move, all_tile_dict)  # Revert move
                        place_value = value - self.piece_values[piece.piece_type]  # General value for placing piece
                elif position[0] in range (-20, 0) and place_piece:
                    value = place_value + self.piece_values[piece.piece_type]
                else:
                    for move in moves:
                        self.move_piece(piece, position, move, all_tile_dict)
                        _, value = self.minimax_with_pruning(game, tiles, tile_dict, all_tiles, all_tile_dict, depth - 1, alpha,beta,False , start_time)
                        self.undo_move(piece, position, move, all_tile_dict)
                alpha = float(alpha)
                beta = float(beta)
                alpha = max(alpha, value)
                value = int(value)
                if value >= best_value:
                    best_value = value
                    best_move = (piece, position, move)
                if beta <= alpha:
                    print(f"beta cut off: ({alpha}) , {beta})") # Beta cut-off
                    break

            return best_move, best_value
        else:
            valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict, all_tiles, "BLACK")
            best_value = float("inf")
            for (piece, position), moves in valid_moves.items():
                if position[0] in range (-20, 0) and not place_piece:
                    place_piece = True
                    for move in moves:
                        self.move_piece(piece, position, move, all_tile_dict)
                        _, value = self.minimax_with_pruning(game, tiles, tile_dict, all_tiles, all_tile_dict, depth - 1, alpha,beta,True , start_time)
                        self.undo_move(piece, position, move, all_tile_dict)  # Revert move
                        place_value = value + self.piece_values[piece.piece_type]  # General value for placing piece
                elif position[0] in range (-20, 0) and place_piece:
                    value = place_value - self.piece_values[piece.piece_type]
                else:
                    for move in moves:
                        self.move_piece(piece, position, move, all_tile_dict)
                        _, value = self.minimax_with_pruning(game, tiles, tile_dict, all_tiles, all_tile_dict, depth - 1, alpha,beta,False, start_time)
                        self.undo_move(piece, position, move, all_tile_dict)
                beta = float(beta)
                alpha = float(alpha)
                beta = min(beta, value)
                if value <= best_value:
                    best_value = value
                    best_move = (piece, position, move)
                if beta <= alpha:
                    print(f"alpha cut off: ({alpha}) , {beta})")
                    break  # Alpha cut-off

            return best_move, best_value

    def iterative_deepening(self,game, tiles, tile_dict, all_tiles, all_tile_dict, max_depth, maximizing_player, start_time):
        best_move = None
        for depth in range(1, max_depth + 1):
            if maximizing_player:
                best_move, value = self.minimax_with_pruning(game, tiles, tile_dict, all_tiles, all_tile_dict, depth, "-inf", "inf", True, start_time)
            else:
                best_move, value = self.minimax_with_pruning(game, tiles, tile_dict, all_tiles, all_tile_dict, depth, "-inf", "inf", False, start_time)
            print(f"Depth: {depth}, Best move: {best_move}, Value: {value}")
        return best_move , value

    def ai_move(self, game, tiles, tile_dict, all_tiles, all_tile_dict):
        piece = None
        position = None
        move = None
        best_value = 1000
        start_time = time.time()
        best_move = False
        valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict, all_tiles, self.color)
        if self.color == "BLACK":
            for (piece, position), moves in valid_moves.items():
                for move in moves:
                    self.move_piece(piece, position, move, all_tile_dict)
                    _,value = self.minimax(game, tiles, tile_dict, all_tiles, all_tile_dict, self.difficulty, False,start_time)
                    self.undo_move(piece, position, move, all_tile_dict)
                    if value < best_value:
                        best_value = value
                        best_move = (piece, all_tile_dict[position], tile_dict[move])
            return best_move
        elif self.color == "WHITE":
            (piece, position, move), value = self.minimax(game, tiles, tile_dict, all_tiles, all_tile_dict, self.difficulty, True, start_time)
        best_move = (piece, all_tile_dict[position], tile_dict[move])
        return best_move
