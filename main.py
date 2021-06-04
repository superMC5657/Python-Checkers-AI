# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import random

import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax, alphabeta, random_move

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


difficult_dict = {1: (alphabeta, 2), 2: (alphabeta, 4), 3: (minimax, 4)}


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    game_level = int(input('plz choose ai level! 1:low,2:medium,3:hard, you choose:'))
    func, depth = difficult_dict[game_level]
    print('Rules：')
    print('--------------------------------')
    print('Forced Captures: When a player is in a position to make a capturing move, he must make a capturing move. \n'
          'When he has more than one capturing move to choose from he may take whichever move suits him.')
    print('--------------------------------')
    print("Crowning King in Checkers: When a checker achieves the opponent's edge of the board (called the 'king s \n"
          "row') it is crowned with another checker. This signifies that the checker has been made a king. The king now \n"
          "gains an added ability to move backward. The king may now also jump in either direction or even in both \n"
          "directions in one turn (if he makes multiple jumps).")
    while run:
        clock.tick(FPS)

        # if game.turn == WHITE:
        #     if random.randint(0, 5) == 1:
        #         value, new_board = random_move(game.get_board(), depth, WHITE, game)
        #     else:
        #         value, new_board = func(game.get_board(), depth, WHITE, game)
        #     game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()


main()
