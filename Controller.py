from hex import hex_neighbors
import pygame
def place_piece(piece, tiles):
    my_neighbors = set()
    opposing_neighbors = set()
    for tile in tiles:
        if tile.has_pieces():
            if tile.pieces[0].color == piece.color:
                my_neighbors.update(hex_neighbors(tile.position))
            else:
                opposing_neighbors.update(hex_neighbors(tile.position))
                opposing_neighbors.update([tile.position])  # Add the tile itself
    # Ensure the same tile can't have more than one piece
    valid_moves = [move for move in my_neighbors - opposing_neighbors if not any(tile.position == move and tile.has_pieces() for tile in tiles)]
    return valid_moves

def is_piece_on_board(piece, tiles):
    for tile in tiles:
        if piece.position == tile.position:
            return True
    return False

def is_queen_on_board(color, tiles):
    for tile in tiles:
        if tile.has_pieces():
            for piece in tile.pieces:
                if piece.piece_type == "Queen Bee" and piece.color == color:
                    return True
    return False

def is_queen_surrounded(piece, tile_dict):
    queen_bees = []
    
    # Find all neighboring queen bees
    for neighbor_pos in hex_neighbors(piece.position):
        neighbor_tile = tile_dict.get(neighbor_pos)
        if neighbor_tile and neighbor_tile.has_pieces():
            for neighbor_piece in neighbor_tile.pieces:
                if neighbor_piece.piece_type == "Queen Bee":
                    queen_bees.append(neighbor_piece)
    
    # Check if each queen bee is surrounded
    surrounded_queens = []
    for queen in queen_bees:
        queen_surrounded = True
        for neighbor_pos_queen in hex_neighbors(queen.position):
            neighbor_tile_queen = tile_dict.get(neighbor_pos_queen)
            if not neighbor_tile_queen or not neighbor_tile_queen.has_pieces():
                queen_surrounded = False
                break
        if queen_surrounded:
            surrounded_queens.append(queen.color)
    
    if len(surrounded_queens) == 2:
        return "tie"
    elif len(surrounded_queens) == 1:
        return surrounded_queens[0]
    else:
        return False

def is_hive_connected(tiles):
    visited = set()
    start_tile = None

    # Find a starting tile with pieces
    for tile in tiles:
        if tile.has_pieces():
            start_tile = tile
            break

    if not start_tile:
        return True  # No pieces on the board, so it's trivially connected

    # Perform a BFS or DFS to check connectivity
    def dfs(tile):
        if tile in visited:
            return
        visited.add(tile)
        for neighbor_pos in hex_neighbors(tile.position):
            for neighbor_tile in tiles:
                if neighbor_tile.position == neighbor_pos and neighbor_tile.has_pieces():
                    dfs(neighbor_tile)

    dfs(start_tile)

    # Check if all tiles with pieces have been visited
    for tile in tiles:
        if tile.has_pieces() and tile not in visited:
            return False

    return True

def filter_moves(piece, valid_moves, tiles):
    if is_piece_on_board(piece, tiles):
        original_position = piece.position
        filtered_moves = []
        # Temporarily remove the piece from its original position
        original_tile = next(tile for tile in tiles if tile.position == original_position)
        original_tile.pieces.remove(piece)
        if is_hive_connected(tiles):
            for move in valid_moves:
                # Move the piece to the new position
                new_tile = next(tile for tile in tiles if tile.position == move)
                new_tile.pieces.append(piece)
                if is_hive_connected(tiles):
                    filtered_moves.append(move)
                new_tile.pieces.remove(piece)

        # Revert the piece to its original position
        original_tile.pieces.append(piece)
        return filtered_moves
    else:
        return valid_moves

def get_valid_moves(piece, game, tiles, tile_dict):
    valid_moves = []
    if game.turn == 1:
        valid_moves = [(7, 17)]
    elif game.turn == 2:
        valid_moves = hex_neighbors((7, 17))
    elif game.turn in (3, 4):
        # Only allow selecting pieces from inventory
        if not is_piece_on_board(piece, tiles):
            valid_moves = place_piece(piece, tiles)
    elif game.turn in (5, 6):
        if is_queen_on_board(piece.color, tiles):
            valid_moves = piece.valid_moves(tiles, tile_dict)
        else:
            # Only allow selecting pieces from inventory
            if not is_piece_on_board(piece, tiles):
                valid_moves = place_piece(piece, tiles)
    elif game.turn in (7, 8):
        if is_queen_on_board(piece.color, tiles):
            valid_moves = piece.valid_moves(tiles, tile_dict)
        else:
            # Only allow selecting the queen from inventory
            if piece.piece_type == "Queen Bee" and piece.color == game.current_state:
                valid_moves = place_piece(piece, tiles)
    else:
        valid_moves = piece.valid_moves(tiles, tile_dict)

    # Filter out moves that break the hive
    valid_moves = filter_moves(piece, valid_moves, tiles)

    return valid_moves

def can_slide_out(neighbors, tiles):
    free_spaces = []
    valid_spaces = set()  # Use a set to avoid duplicates
    for neighbor_pos in neighbors:
        neighbor_tile = next((t for t in tiles if t.position == neighbor_pos), None)
        if not neighbor_tile or not neighbor_tile.has_pieces():
            free_spaces.append(neighbor_pos)
        
    # Check if there are at least two adjacent free spaces
    for i in range(len(free_spaces)):
        for j in range(i + 1, len(free_spaces)):
            if free_spaces[i] in hex_neighbors(free_spaces[j]):
                valid_spaces.add(free_spaces[i])
                valid_spaces.add(free_spaces[j])
    return list(valid_spaces)

def can_slide_in(position, tiles, piece):
    #Todo
    pass

def generate_adjacent_moves(position, tile_dict):
    valid_moves = []
    neighbors = hex_neighbors(position)
    
    for i in range(len(neighbors)):
        neighbor_pos = neighbors[i]
        next_index = (i + 1) % len(neighbors)
        next_neighbor_pos = neighbors[next_index]
        
        if neighbor_pos in tile_dict and tile_dict[neighbor_pos].has_pieces():
            if next_neighbor_pos in tile_dict and not tile_dict[next_neighbor_pos].has_pieces():
                valid_moves.append(next_neighbor_pos)
        elif neighbor_pos in tile_dict and not tile_dict[neighbor_pos].has_pieces():
            if next_neighbor_pos in tile_dict and tile_dict[next_neighbor_pos].has_pieces():
                valid_moves.append(neighbor_pos)
    
    return valid_moves

def get_all_valid_moves_for_color(game, tiles, tile_dict,color):
    valid_moves = {}
    for tile in tiles:
        if tile.has_pieces() and tile.pieces[-1].color == color:
            valid_moves[(tile.pieces[-1],tile.position)] = get_valid_moves(tile.pieces[-1], game, tiles, tile_dict)
    return valid_moves

def move_piece(piece,old_position,newPosition,tiles):
    for tile in tiles:
        if tile.has_pieces() and tile.position == old_position and tile.pieces[0] == piece:
            # print("old found")
            tile.remove_piece()
            break
    for tile in tiles:
        if tile.position == newPosition:
            # print("new found")

            tile.add_piece(piece)
            break
def undo_move(piece, old_position, new_position, tiles):
    for tile in tiles:
        if tile.position == new_position and piece in tile.pieces:
            tile.remove_piece()
            break
    for tile in tiles:
        if tile.position == old_position:
            tile.add_piece(piece)
            break
def count_queenbee_black_surronded(tiles_dict):
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
def count_queenbee_white_surronded(tiles_dict):
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

# def scoreBoard(all_tiles,tile_dict):
#     total_score_white =0
#     total_score_black =0
#     for tile in all_tiles:
#         for piece in tile.pieces:
#             if piece.piece_type == "Solider Ant" and piece.color == "WHITE":
#                 total_score_white +=60
#             elif piece.piece_type == "Beetle" and piece.color == "WHITE":
#                 total_score_white +=80
#             elif piece.piece_type == "Grasshopper" and piece.color == "WHITE":
#                 total_score_white +=30
#             elif piece.piece_type == "Spider" and piece.color == "WHITE":
#                 total_score_white +=40
#             elif piece.piece_type == "Beetle" and piece.color == "BLACK":
#                 total_score_black +=80
#             elif piece.piece_type == "Grasshopper" and piece.color == "BLACK":
#                 total_score_black +=30
#             elif piece.piece_type == "Spider" and piece.color == "BLACK":
#                 total_score_black +=40
#             elif piece.piece_type == "Solider Ant" and piece.color == "BLACK":
#                 total_score_black +=60

#     black_surronded = count_queenbee_black_surronded(tile_dict)
#     white_surronded = count_queenbee_white_surronded(tile_dict)

#     #print("score from board",20*(total_score_white-total_score_black)+30*(black_surronded-white_surronded))

#     return 20*(total_score_white-total_score_black)+30*(black_surronded-white_surronded)

# def board_value(game, all_tiles,tile_dict):
#     result = scoreBoard(all_tiles,tile_dict)
#     if game.current_state == "BLACK":
#         return result * -1
#     return result


# New Scoring

def count_pieces(tile_dict, color):
    count = 0
    for tile in tile_dict.values():
        for piece in tile.pieces:
            if piece.color == color:
                count += 1
    return count

def count_valid_moves(game, tiles, tile_dict, color):
    valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict,color)
    move_count = sum(len(moves) for moves in valid_moves.values())
    return move_count

def piece_value(piece):
    if piece.piece_type == "Queen Bee":
        return 1
    elif piece.piece_type == "Beetle":
        return 3
    elif piece.piece_type == "Soldier Ant":
        return 10
    elif piece.piece_type == "Grasshopper":
        return 7
    elif piece.piece_type == "Spider":
        return 5
    return 0

def evaluate_pieces(tile_dict, color):
    value = 0
    for tile in tile_dict.values():
        for piece in tile.pieces:
            if piece.color == color:
                value += piece_value(piece)
    return value

def scoreBoard(game, tiles, tile_dict):
    black_surrounded = count_queenbee_black_surronded(tile_dict)
    white_surrounded = count_queenbee_white_surronded(tile_dict)

    black_piece_count = count_pieces(tile_dict, "BLACK")
    white_piece_count = count_pieces(tile_dict, "WHITE")

    black_move_count = count_valid_moves(game, tiles, tile_dict, "BLACK")
    white_move_count = count_valid_moves(game, tiles, tile_dict, "WHITE")

    black_piece_value = evaluate_pieces(tile_dict, "BLACK")
    white_piece_value = evaluate_pieces(tile_dict, "WHITE")

    # Heuristic weights
    queen_surround_weight = 10
    piece_count_weight = 1
    move_count_weight = 1
    piece_value_weight = 2

    score = (queen_surround_weight * (black_surrounded - white_surrounded) +
             piece_count_weight * (black_piece_count - white_piece_count) +
             move_count_weight * (black_move_count - white_move_count) +
             piece_value_weight * (black_piece_value - white_piece_value))
    #print("score from board",score)

    return score

def board_value(game, all_tiles,tile_dict):
    result = scoreBoard(game,all_tiles,tile_dict)
    if game.current_state == "BLACK":
        return result * -1
    return result


def minimax(game, tiles, tile_dict, depth, maximizing_player):
    global best_move
    global best_value
    if depth == 0:
        return board_value(game, tiles, tile_dict)

    if maximizing_player:
        valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict,"WHITE")
    else:
        valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict,"BLACK")
    #print(valid_moves)
    if maximizing_player:
        best_value = -1000
        for (piece, position), moves in valid_moves.items():
            for move in moves:
                move_piece(piece, position, move, tiles)
                value = minimax(game, tiles, tile_dict, depth - 1, False)
                #print("value retured from minimax",value)
                undo_move(piece, position, move, tiles) # Revert move

                if value > best_value:
                    #print("best_value before", best_value)
                    best_value = value
                    #print("best_value after",best_value)
                    best_move = (piece, position, move)
        return best_value

    else:
        best_value = 1000
        for (piece, position), moves in valid_moves.items():
            for move in moves:
                move_piece(piece, position, move, tiles)
                value = minimax(game, tiles, tile_dict, depth - 1, True)
                undo_move(piece, position, move, tiles)  # Revert move
                if value < best_value:
                    best_value = value
                    best_move = (piece, position, move)

        return best_value

def minimax_with_pruning(game, tiles, tile_dict, depth, alpha, beta, maximizing_player):
    if depth == 0 or game.is_game_over:
        return board_value(game, tile_dict)

    valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict)
    if maximizing_player:
        best_value = -1000
        for (piece, position), moves in valid_moves.items():
            for move in moves:
                move_piece(piece, position, move, tiles)
                value = minimax_with_pruning(game, tiles, tile_dict, depth - 1, alpha, beta, False)
                undo_move(piece, position, move, tiles)  # Revert move
                best_value = max(best_value, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cut-off
        return best_value
    else:
        best_value = 1000
        for (piece, position), moves in valid_moves.items():
            for move in moves:
                move_piece(piece, position, move, tiles)
                value = minimax_with_pruning(game, tiles, tile_dict, depth - 1, alpha, beta, True)
                undo_move(piece, position, move, tiles)  # Revert move
                best_value = min(best_value, value)
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cut-off
        return best_value
    
def ai_move(game, tiles, tile_dict, depth=4):
    best_value = 1000
    best_move = None
    valid_moves = get_all_valid_moves_for_color(game, tiles, tile_dict,game.current_state)

    for (piece, position), moves in valid_moves.items():
        for move in moves:
            move_piece(piece, position, move, tiles)
            value = minimax(game, tiles, tile_dict, depth, True)
            undo_move(piece, position, move, tiles)
            if value < best_value:
                best_value = value
                
                best_move = (tile_dict[position], tile_dict[move])

    return best_move

def humen_move(game,tiles,tile_dict,clicked_tile,selected_tile,loser_color,turn_panel,screen,timer,valid_moves,piece):
    if selected_tile is None:
        if clicked_tile.pieces:
            # Check if the piece belongs to the current player
            piece = clicked_tile.pieces[-1]
            if game.current_state == piece.color:
                selected_tile = clicked_tile
                selected_tile.selected()
                valid_moves = get_valid_moves(
                    piece, game, tiles, tile_dict)
                for move in valid_moves:
                    for tile in tiles:
                        if move == tile.position:
                            tile.highlight()
    else:
        if selected_tile != clicked_tile and clicked_tile.position in valid_moves:
            selected_tile.move_piece(clicked_tile)
            queen_color = is_queen_surrounded(piece, tile_dict)
            if queen_color:

                loser_color = queen_color
                game.is_game_over=True
                pygame.time.delay(200)

            game.change_turn()
            turn_panel.update(screen, game.current_state)
            timer.reset_timer()
        selected_tile.unhighlight()
        selected_tile = None
        for tile in tiles:
            tile.unhighlight()
    return (selected_tile,loser_color,valid_moves,piece)

