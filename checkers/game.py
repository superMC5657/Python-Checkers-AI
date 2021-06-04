import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    # update canvas
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    # when people select a piece,
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    # Crowning King in Checkers when a king is killed, killer become the other king.
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                for s in skipped:
                    if s.king:
                        self.selected.make_king()
                        if self.selected.color == WHITE:
                            self.board.white_kings += 1
                        else:
                            self.board.red_kings += 1
                        break
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    # when piece in Forced Captures status, flag is False
    def draw_valid_moves(self, moves):
        flag = True
        for move in moves:
            row, col = move
            skipped = moves[move]
            if skipped:
                pygame.draw.circle(self.win, BLUE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
                flag = False
        if flag:
            for move in moves:
                row, col = move
                pygame.draw.circle(self.win, BLUE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    # change turn
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    # AI move in the board
    def ai_move(self, board):
        self.board = board
        self.change_turn()
