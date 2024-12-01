class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color
        self.position = None

    def __repr__(self):
        return f"{self.color} {self.piece_type}"

class Board:
    def __init__(self):
        self.board = {}
        self.pieces = []

    def add_piece(self, piece, position):
        if position in self.board:
            raise ValueError("Position already occupied")
        self.board[position] = piece
        piece.position = position
        self.pieces.append(piece)

    def move_piece(self, piece, new_position):
        if new_position in self.board:
            raise ValueError("Position already occupied")
        del self.board[piece.position]
        self.board[new_position] = piece
        piece.position = new_position

    def __repr__(self):
        return str(self.board)
    
class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = "White"
        self.winner = None

    def place_piece(self, piece_type, position):
        piece = Piece(piece_type, self.current_turn)
        self.board.add_piece(piece, position)
        self.switch_turn()

    def move_piece(self, piece, new_position):
        self.board.move_piece(piece, new_position)
        self.switch_turn()

    def switch_turn(self):
        self.current_turn = "Black" if self.current_turn == "White" else "White"

    def __repr__(self):
        return f"Turn: {self.current_turn}\nBoard:\n{self.board}"