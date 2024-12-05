from hex import hex_neighbors

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

def is_queen_surrounded(piece, tiles):
    for neighbor_pos in hex_neighbors(piece.position):
        neighbor_tile = next((t for t in tiles if t.position == neighbor_pos), None)
        if neighbor_tile and neighbor_tile.has_pieces():
            for neighbor_piece in neighbor_tile.pieces:
                if neighbor_piece.piece_type == "Queen Bee":
                    for neighbor_pos_queen in hex_neighbors(neighbor_tile.position):
                        neighbor_tile_queen = next((t for t in tiles if t.position == neighbor_pos_queen), None)
                        if not neighbor_tile_queen.has_pieces():
                            return False
                    return neighbor_piece.color
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
                for neighbor_pos in hex_neighbors(new_tile.position):
                    for neighbor_tile in tiles:
                        if neighbor_tile.position == neighbor_pos and neighbor_tile.has_pieces():
                            filtered_moves.append(move)
                            break
                new_tile.pieces.remove(piece)
        
        # Revert the piece to its original position
        original_tile.pieces.append(piece)
        return filtered_moves
    else:
        return valid_moves

def get_valid_moves(piece, game, tiles, white_inventory, black_inventory):
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
            valid_moves = piece.valid_moves(tiles)
        else:
            # Only allow selecting pieces from inventory
            if not is_piece_on_board(piece, tiles):
                valid_moves = place_piece(piece, tiles)
    elif game.turn in (7, 8):
        if is_queen_on_board(piece.color, tiles):
            valid_moves = piece.valid_moves(tiles)
        else:
            # Only allow selecting the queen from inventory
            if piece.piece_type == "Queen Bee" and piece.color == game.current_state:
                valid_moves = place_piece(piece, tiles)
    else:
        valid_moves = piece.valid_moves(tiles)

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
