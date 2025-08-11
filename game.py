import pygame

from const import *
from board import Board
from dragger import Dragger
class Game:
    def __init__(self):
        self.next_turn="white"
        self.board=Board()
        self.dragger=Dragger()
        self.font = pygame.font.SysFont('monospace', 14, bold=True)
    def show_notation(self, surface):
            for row in range(ROWS):
                for col in range(COLS):       
                    if col == 0:
                        color = (46, 111, 64) if row % 2 == 0 else (136, 231, 136)
                        lbl = self.font.render(str(ROWS - row), 1, color)
                        lbl_pos = (3, 5 + row * SQSIZE)
                        surface.blit(lbl, lbl_pos)                   
                    if row == 7:
                        color = (46, 111, 64) if (row + col) % 2 == 0 else (136, 231, 136)
                        lbl = self.font.render(chr(ord('a') + col), 1, color)
                        lbl_pos = (col * SQSIZE + SQSIZE - 10, HEIGHT - 17)
                        surface.blit(lbl, lbl_pos)
    def show_bg(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row+col)%2==0:
                    color=(136,231,136)
                else:
                    color=(46,111,64)
                rect=(col*SQSIZE,row*SQSIZE,SQSIZE,SQSIZE)
                pygame.draw.rect(surface,color,rect)
    def show_pieces(self,surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece=self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img=pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect=img.get_rect(center=img_center)
                        surface.blit(img,piece.texture_rect)
    def show_moves(self,surface):
        if self.dragger.dragging:
            piece=self.dragger.piece
            for move in piece.moves:
                color="#791a1aaa" if (move.final.row + move.final.col) % 2 == 0 else "#791a1aaa"
                rect=(move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:              
                color = (244, 247, 116) 
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)               
                pygame.draw.rect(surface, color, rect)
    
    def next_player(self):
        if self.next_turn == "white":
            self.next_turn = "black"
        else:
            self.next_turn = "white"
