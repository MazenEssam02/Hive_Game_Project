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