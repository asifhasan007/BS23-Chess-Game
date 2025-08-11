from const import *
from square import Square
from piece import *
from move import Move
import copy
class Board:

    def __init__(self):
        self.squares=[[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_move=None
    def evaluate(self):
        value = 0
        for row in self.squares:
            for sq in row:
                if sq.has_piece():
                    value += sq.piece.value 
        #punishment
        if self.is_in_check('white'):
            value -= 0.5 
        if self.is_in_check('black'):
            value += 0.5 

        return value 
    def all_moves(self, color):
        moves = []
        for row in range(8):
            for col in range(8):
                sq = self.squares[row][col]
                if sq.has_piece() and sq.piece.color == color:
                    self.calc_moves(sq.piece, row, col)
                    moves.extend([(sq.piece, move) for move in sq.piece.moves])
        return moves
    def copy_board(self):
        return copy.deepcopy(self)
    def move(self, piece, move):
            initial = move.initial
            final = move.final
            
            if self.squares[final.row][final.col].has_piece():
                if self.squares[final.row][final.col].piece.name == 'king':
                    return 

            self.squares[initial.row][initial.col].piece = None
            self.squares[final.row][final.col].piece = piece
         
            if piece.name == 'pawn':
                if final.row == 0 or final.row == 7:
                    self.squares[final.row][final.col].piece = Queen(piece.color)

            piece.moved = True
            piece.clear_moves()
            self.last_move = move
    def add_legal_move(self, piece, move, piece_moves_list):
        
        temp_board = self.copy_board()
        temp_piece = temp_board.squares[move.initial.row][move.initial.col].piece
        temp_board.move(temp_piece, move)

        if not temp_board.is_in_check(piece.color):
            piece_moves_list.append(move)
    def valid_move(self, piece, move):
        return move in piece.moves
    def _create(self):
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col]=Square(row,col)
    def calc_moves(self, piece, row, col, validate_check=True):
        piece.clear_moves()
        def king_moves():
            possible_moves = [
                (row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1),
                (row + 1, col + 1), (row + 1, col - 1), (row - 1, col + 1), (row - 1, col - 1)
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if validate_check:
                            self.add_legal_move(piece, move, piece.moves)
                        else:
                            piece.add_move(move)

        def pawn_moves():
            if piece.moved:
                steps = 1
            else:
                steps = 2
            #vertical moves
            start= row + piece.dir
            end= row + (piece.dir * (1+steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        move = Move(initial, final)
                        if validate_check:
                            self.add_legal_move(piece, move, piece.moves)
                        else:
                            piece.add_move(move)
                    else:
                        break
                else:
                    break
            #diagonal moves
            move_row = row + piece.dir
            move_col= [col - 1, col + 1 ]
            for move_col in move_col:
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        move = Move(initial, final)
                        if validate_check:
                            self.add_legal_move(piece, move, piece.moves)
                        else:
                            piece.add_move(move)
        def knight_moves():
            possible_moves = [
                (row+2, col+1), (row+2, col-1), (row+1, col-2),
                (row+1, col+2), (row-1, col-2), (row-1, col+2),
                (row-2, col-1), (row-2, col+1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
               
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if validate_check:
                            self.add_legal_move(piece, move, piece.moves)
                        else:
                            piece.add_move(move)

        def straight_moves(incrs):
            for incr in incrs:
                incr_row, incr_col = incr
                move_row, move_col = row + incr_row, col + incr_col
                while True:                   
                    if not Square.in_range(move_row, move_col):
                        break                  
                    initial = Square(row, col)
                    final_piece = self.squares[move_row][move_col].piece
                    final = Square(move_row, move_col, final_piece)
                    move = Move(initial, final)
                
                    if self.squares[move_row][move_col].isempty():
                        if validate_check:
                            self.add_legal_move(piece, move, piece.moves)
                        else:
                            piece.add_move(move)                    
                    
                    elif self.squares[move_row][move_col].has_enemy_piece(piece.color):
                        if validate_check:
                            self.add_legal_move(piece, move, piece.moves)
                        else:
                            piece.add_move(move)
                        break 
            
                    elif self.squares[move_row][move_col].has_team_piece(piece.color):
                        break 
                    move_row += incr_row
                    move_col += incr_col

        if isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, King):
            king_moves()
        elif isinstance(piece, Rook):
            straight_moves([(1, 0), (-1, 0), (0, 1), (0, -1)])
        elif isinstance(piece, Bishop):
            straight_moves([(1, 1), (1, -1), (-1, 1), (-1, -1)])
        elif isinstance(piece, Queen):
            straight_moves([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])
            



    def _add_pieces(self, color):
            row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

            # pawns
            for col in range(COLS):
                self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
              
            
            # knights
            self.squares[row_other][1] = Square(row_other, 1, Knight(color))
            self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        

            # bishops
            self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
            self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
            

            # rooks
            self.squares[row_other][0] = Square(row_other, 0, Rook(color))
            self.squares[row_other][7] = Square(row_other, 7, Rook(color))
           
            # queen
            self.squares[row_other][3] = Square(row_other, 3, Queen(color))
            

            # king
            self.squares[row_other][4] = Square(row_other, 4, King(color))
    
    def find_king(self, color):
        
        for row in range(8):
            for col in range(8):
                sq = self.squares[row][col]
                if sq.has_piece() and sq.piece.name == 'king' and sq.piece.color == color:
                    return (row, col)
        return None

    def is_in_check(self, color):
    
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        king_row, king_col = king_pos
        
        for row in range(8):
            for col in range(8):
                sq = self.squares[row][col]
                if sq.has_piece() and sq.piece.color != color:
                    self.calc_moves(sq.piece, row, col, validate_check=False)
                    for move in sq.piece.moves:
                        if move.final.row == king_row and move.final.col == king_col:
                            return True
        return False

    def has_legal_move(self, color):
        
        for row in range(8):
            for col in range(8):
                sq = self.squares[row][col]
                if sq.has_piece() and sq.piece.color == color:
                   
                    self.calc_moves(sq.piece, row, col)
                  
                    for move in sq.piece.moves:
                        
                        temp_board = self.copy_board()
                                               
                        temp_piece = temp_board.squares[row][col].piece
                                               
                        temp_board.move(temp_piece, move)
                        if not temp_board.is_in_check(color):
                            return True 

        return False



    def checkmate(self, color):
        return self.is_in_check(color) and not self.has_legal_move(color)

    def stalemate(self, color):
        return (not self.is_in_check(color)) and (not self.has_legal_move(color))


def minimax(board, depth, maximizing, alpha, beta):
    if depth == 0 or board.checkmate('white') or board.checkmate('black') or board.stalemate('white') or board.stalemate('black'):
        return board.evaluate(), None

    color = 'white' if maximizing else 'black'
    
    moves = board.all_moves(color)
    moves.sort(key=lambda item: board.squares[item[1].final.row][item[1].final.col].has_piece(), reverse=True)

    best_move = None

    if maximizing:
        max_eval = float('-inf')
        
        for piece, move in moves:
            temp_board = board.copy_board()
            temp_board.move(piece, move)
            eval, _ = minimax(temp_board, depth - 1, False, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = (piece, move)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break 
        return max_eval, best_move
    else: 
        min_eval = float('inf')
        
        for piece, move in moves:
            temp_board = board.copy_board()
            temp_board.move(piece, move)
            eval, _ = minimax(temp_board, depth - 1, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = (piece, move)
            beta = min(beta, eval)
            if beta <= alpha:
                break 
        return min_eval, best_move

               