import pygame
import sys

from const import *
from game import Game
from board import Board
from square import Square
from dragger import Dragger
from piece import Piece
from move import Move
from board import minimax

class Main:

    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode( (WIDTH,HEIGHT) )
        pygame.display.set_caption("BS23 Chess Competition")
        self.game=Game()

    def mainloop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
        while True:
          
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_notation(screen) 
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                game.show_notation(screen) 
                dragger.update_blit(screen)
               

            # AI logic 
            if game.next_turn == 'black':
                
                if board.checkmate('black'):
                    print("Checkmate! Black loses.")
                    pygame.time.wait(3000) 
                    pygame.quit()
                    sys.exit()
                elif board.stalemate('black'):
                    print("Stalemate! It's a draw.")
                    pygame.time.wait(3000)
                    pygame.quit()
                    sys.exit()

                
                print("AI is processing move")
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_notation(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                font = pygame.font.SysFont('monospace', 40, bold=True)
                thinking_text = font.render("AI is processing move!", True, (191, 6, 6))
                screen.blit(thinking_text, (WIDTH//2 - thinking_text.get_width()//2, HEIGHT//2))
                pygame.display.update()

                t1, best_move = minimax(board, 1, False, float('-inf'), float('inf'))  # example with deeper depth


                if best_move:
                    ai_piece, ai_move = best_move
                    board.move(ai_piece, ai_move)
                                       
                    if board.is_in_check('white'):
                        print("White is in check!")

                    game.next_player() 
                                
                game.show_bg(screen)
                
                game.show_pieces(screen)
            if game.next_turn == 'white':
                if board.checkmate('white'):
                    print("Checkmate! White loses.")
                    pygame.time.wait(3000) 
                    pygame.quit()
                    sys.exit()
                elif board.stalemate('white'):
                    print("Stalemate! It's a draw.")
                    pygame.time.wait(3000)
                    pygame.quit()
                    sys.exit()

            for event in pygame.event.get():
                
                if game.next_turn == 'white':
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)
                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece
                            if piece.color == 'white':
                                board.calc_moves(piece, clicked_row, clicked_col)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)
                                game.show_bg(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)

                    elif event.type == pygame.MOUSEMOTION:
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_notation(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            dragger.update_blit(screen)

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            if board.valid_move(dragger.piece, move):
                                board.move(dragger.piece, move)
                                                    
                                if board.is_in_check('black'):
                                    print("Black is in check!")                               
                                game.next_player()                                
                            dragger.undrag_piece()
        
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
main=Main()
main.mainloop()