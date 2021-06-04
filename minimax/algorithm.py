import sys
from copy import deepcopy
import pygame

RED = (255, 0, 0)
WHITE = (255, 255, 255)


# AI move use minimax with alphabeta
def alphabeta(position, depth, max_player, game, alpha=-sys.maxsize, beta=sys.maxsize):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position

    if max_player:
        maxEval = -sys.maxsize
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation, _ = alphabeta(move, depth - 1, False, game, alpha, beta)
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break

        return maxEval, best_move
    else:
        minEval = sys.maxsize
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation, _ = alphabeta(move, depth - 1, True, game, alpha, beta)
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            beta = min(beta, minEval)
            if beta <= alpha:
                break

        return minEval, best_move


import random


# AI random move function
def random_move(position, depth, max_player, game):
    move_list = get_all_moves(position, max_player, game)
    move = random.choice(move_list)
    return move.evaluate(), move


# AI move use minimax
def minimax(position, depth, max_player, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


# find all of pieces moves in the board
def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves


# draw valid moves  process
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(100)
