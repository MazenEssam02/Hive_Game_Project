from hex import hex_neighbors
import hex
import pygame

def place_piece(piece, tiles):
    my_neighbors = set()
    opposing_neighbors = set()
    for tile in tiles:
        if tile.has_pieces():
            if tile.pieces[-1].color == piece.color:
                my_neighbors.update(hex_neighbors(tile.position))
            else:
                opposing_neighbors.update(hex_neighbors(tile.position))
                opposing_neighbors.update([tile.position])  # Add the tile itself
    # Ensure the same tile can't have more than one piece
    valid_moves = [move for move in my_neighbors - opposing_neighbors if not any(tile.position == move and tile.has_pieces() for tile in tiles)]

    return valid_moves

def is_piece_on_board(piece, tile_dict):
    if piece.position in tile_dict:
        return True
    return False

def is_queen_on_board(color, tiles):
    for tile in tiles:
        if tile.has_pieces():
            for piece in tile.pieces:
                if piece.piece_type == "Queen Bee" and piece.color == color:
                    return True
    return False

def is_queen_surrounded(color, tile_dict):
    white_queen_surrounded = False
    black_queen_surrounded = False
    white_queen = 0
    black_queen = 0
    if hex.white_queen_position != None and hex.white_queen_position[0] != -20:
        white_queen_surrounded = True
        for neighbor_pos in hex_neighbors(hex.white_queen_position):
            if not tile_dict[neighbor_pos].has_pieces():
                white_queen_surrounded = False
            else:
                white_queen += 1

    if hex.black_queen_position != None and hex.black_queen_position[0] != -10:
        black_queen_surrounded = True
        for neighbor_pos in hex_neighbors(hex.black_queen_position):
            if not tile_dict[neighbor_pos].has_pieces():
                black_queen_surrounded = False
            else:
                black_queen += 1

    if black_queen_surrounded and white_queen_surrounded:
        if color == "WHITE":
            return "BLACK" , white_queen, black_queen
        else:
            return "WHITE" , white_queen, black_queen
    elif white_queen_surrounded:
        return "WHITE" , white_queen, black_queen
    elif black_queen_surrounded:
        return "BLACK" , white_queen, black_queen
    else:
        return False , white_queen, black_queen

def is_hive_connected(tiles, tile_dict):
    visited = set()
    start_tile = None

    # Find a starting tile with pieces
    for tile in tiles:
        if tile.has_pieces():
            start_tile = tile
            break

    if not start_tile:
        return True  # No pieces on the board, so it's trivially connected

    # Perform a DFS to check connectivity
    def dfs(tile):
        if tile in visited:
            return
        visited.add(tile)
        for neighbor_pos in hex_neighbors(tile.position):
            neighbor_tile = tile_dict[neighbor_pos]
            if neighbor_tile and neighbor_tile.has_pieces():
                dfs(neighbor_tile)

    dfs(start_tile)

    # Check if all tiles with pieces have been visited
    for tile in tiles:
        if tile.has_pieces() and tile not in visited:
            return False

    return True

def doesnt_break_hive(piece,tiles, tile_dict):
    original_tile = tile_dict[piece.position]
    original_tile.pieces.remove(piece)
    if is_hive_connected(tiles, tile_dict):
        # Revert the piece to its original position
        original_tile.pieces.append(piece)
        return True
    original_tile.pieces.append(piece)
    return False

def can_slide_out(neighbors, tile_dict):
    free_spaces = []
    valid_indices = set()  # Use a set to avoid duplicates
    for i, neighbor_pos in enumerate(neighbors):
        neighbor_tile = tile_dict.get(neighbor_pos)
        if not neighbor_tile or not neighbor_tile.has_pieces():
            free_spaces.append((i, neighbor_pos))
        
    # Check if there are at least two adjacent free spaces
    for i in range(len(free_spaces)):
        for j in range(i + 1, len(free_spaces)):
            if free_spaces[i][1] in hex_neighbors(free_spaces[j][1]):
                valid_indices.add(free_spaces[i][0])
                valid_indices.add(free_spaces[j][0])
    return list(valid_indices)

def generate_adjacent_moves(position, tile_dict):
    valid_moves = []
    neighbors = hex_neighbors(position)
    free_indices = can_slide_out(neighbors, tile_dict)

    for i in free_indices:
        neighbor_pos = neighbors[i]
        next_index = (i + 1) % len(neighbors)
        next_neighbor_pos = neighbors[next_index]
        previous_index = (i - 1) % len(neighbors)
        previous_neighbor_pos = neighbors[previous_index]
        
        if neighbor_pos in tile_dict and not tile_dict[neighbor_pos].has_pieces() and (
            (next_neighbor_pos in tile_dict and tile_dict[next_neighbor_pos].has_pieces()) or
            (previous_neighbor_pos in tile_dict and tile_dict[previous_neighbor_pos].has_pieces())
        ):
            valid_moves.append(neighbor_pos)
    
    return valid_moves

def get_valid_moves(piece, game, tiles, tile_dict):
    valid_moves = []
    if game.turn == 1:
        valid_moves = [(7, 17)]
    elif game.turn == 2:
        valid_moves = hex_neighbors((7, 17))
    elif game.turn in (3, 4):
        # Only allow selecting pieces from inventory
        if not is_piece_on_board(piece, tile_dict):
            valid_moves = place_piece(piece, tiles)
    elif game.turn in (5, 6):
        if is_queen_on_board(piece.color, tiles):
            valid_moves = piece.valid_moves(tiles, tile_dict)
        else:
            # Only allow selecting pieces from inventory
            if not is_piece_on_board(piece, tile_dict):
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

    return valid_moves

def get_all_valid_moves_for_color(game, tiles, tile_dict, all_tiles, color, piece_type=None):
    valid_moves = {}
    for tile in all_tiles:
        if tile.has_pieces():
            piece = tile.pieces[-1]
            if piece.color == color and (piece_type is None or piece.piece_type == piece_type):
                moves = get_valid_moves(piece, game, tiles, tile_dict)
                if moves:
                    valid_moves[(piece, tile.position)] = moves
    return valid_moves

def human_move(game,tiles,tile_dict, clicked_tile,selected_tile,loser_color,turn_panel,screen,timer,valid_moves,piece):
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
            queen_color = is_queen_surrounded(game.current_state, tile_dict)[0]
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