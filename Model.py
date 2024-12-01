from hex import hex_neighbors
class Board:
    def __init__(self):
        self.board = {}
        self.pieces = []

    def add_piece(self, piece_type, color, position):
        if piece_type == "Queen Bee":
            piece = QueenBee(color)
        elif piece_type == "Beetle":
            piece = Beetle(color)
        elif piece_type == "Grasshopper":
            piece = Grasshopper(color)
        elif piece_type == "Spider":
            piece = Spider(color)
        elif piece_type == "Soldier Ant":
            piece = SoldierAnt(color)
        else:
            raise ValueError("Unknown piece type")

        if position in self.board:
            raise ValueError("Position already occupied")
        self.board[position] = piece
        piece.position = position
        self.pieces.append(piece)

    def move_piece(self, piece, new_position):
        if isinstance(piece, Beetle):
            # Beetle can move over other pieces
            if new_position not in self.board:
                self.board[new_position] = []
        else:
            if new_position in self.board and self.board[new_position]:
                raise ValueError("Position already occupied")
        self.board[piece.position].remove(piece)
        if not self.board[piece.position]:
            del self.board[piece.position]
        self.board[new_position].append(piece)
        piece.position = new_position

    def is_valid_move(self, piece, new_position):
        #Todo
        pass

    def __repr__(self):
        return str(self.board)
    
class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = "White"
        self.winner = None

    def place_piece(self, piece_type, position):
        self.board.add_piece(piece_type, self.current_turn, position)
        self.switch_turn()

    def move_piece(self, piece, new_position):
        if self.board.is_valid_move(piece, new_position):
            self.board.move_piece(piece, new_position)
            self.switch_turn()
        else:
            raise ValueError("Invalid move")

    def switch_turn(self):
        self.current_turn = "Black" if self.current_turn == "White" else "White"

    def __repr__(self):
        return f"Turn: {self.current_turn}\nBoard:\n{self.board}"
    
class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color
        self.position = None

    def __repr__(self):
        return f"{self.color} {self.piece_type}"

class QueenBee(Piece):
    def __init__(self, color):
        super().__init__("Queen Bee", color)

    def valid_moves(self, board):
        # Queen Bee can move one space in any direction
        neighbors = hex_neighbors(self.position)
        return [pos for pos in neighbors if pos not in board.board]
    
class Beetle(Piece):
    def __init__(self, color):
        super().__init__("Beetle", color)

    def valid_moves(self, board):
        # Beetle can move one space in any direction, including on top of other pieces
        neighbors = hex_neighbors(self.position)
        return neighbors
    
class Grasshopper(Piece):
    def __init__(self, color):
        super().__init__("Grasshopper", color)

    def valid_moves(self, board):
        # Grasshopper jumps over pieces in a straight line
        directions = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
        valid_moves = []
        for d in directions:
            pos = (self.position[0] + d[0], self.position[1] + d[1])
            if pos in board.board:
                while pos in board.board:
                    pos = (pos[0] + d[0], pos[1] + d[1])
                valid_moves.append(pos)
        return valid_moves
    
class Spider(Piece):
    def __init__(self, color):
        super().__init__("Spider", color)

    def valid_moves(self, board):
        # Spider moves exactly three spaces
        def dfs(position, depth, visited):
            if depth == 3:
                return [position]
            moves = []
            for neighbor in hex_neighbors(position):
                if neighbor not in visited and neighbor in board.board:
                    # Check if the neighbor is adjacent to the hive
                    if any(adj in board.board for adj in hex_neighbors(neighbor)):
                        visited.add(neighbor)
                        moves.extend(dfs(neighbor, depth + 1, visited))
                        visited.remove(neighbor)
            return moves

        visited = {self.position}
        return dfs(self.position, 0, visited)

class SoldierAnt(Piece):
    def __init__(self, color):
        super().__init__("Soldier Ant", color)

    def valid_moves(self, board):
        # Soldier Ant can move to any position around the hive
        def bfs(start):
            queue = [start]
            visited = {start}
            moves = []
            while queue:
                position = queue.pop(0)
                for neighbor in hex_neighbors(position):
                    if neighbor not in visited and neighbor not in board.board:
                        # Check if the neighbor is adjacent to the hive
                        if any(adj in board.board for adj in hex_neighbors(neighbor)):
                            visited.add(neighbor)
                            queue.append(neighbor)
                            moves.append(neighbor)
            return moves

        return bfs(self.position)