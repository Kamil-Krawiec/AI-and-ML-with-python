from copy import deepcopy
from time import process_time

from Lab02.Heuristics import *
from Lab02.Reversi import *
from Lab02.Player import Player

# BLACK always go first.
# WHITE always go second.
player1 = Player('1',heuristic=heuristic2,maxDepth=2)
player2 = Player('2',heuristic=heuristic3,maxDepth=2)

def minimaxi():
    board = Reversi(black=player1, white=player2, start_from_round=4)

    print(board)

    s = process_time()
    while board.game_state == 'In progress':
        if board.player == '1':
            score, coord = player1.make_best_move(deepcopy(board))
            board.play(coord)
        else:
            score, coord = player2.make_best_move(deepcopy(board))
            board.play(coord)

    e = process_time()

    print(board)
    print(f'{board.game_state} won with score {board.custom_player_discs_len(board.game_state)}')

    loser = player1.field if board.game_state != player1.field else player2.field

    print(f'{loser} lost with score {board.custom_player_discs_len(loser)}')

    print(f'{e - s}s duration')

def minimaxi_alpha_beta():
    board = Reversi(black=player1, white=player2, start_from_round=4)

    print(board)
    s = process_time()
    while board.game_state == 'In progress':
        if board.player == '1':
            score, coord = player1.make_best_move_alpha_beta(deepcopy(board))
            board.play(coord)
        else:
            score, coord = player2.make_best_move_alpha_beta(deepcopy(board))
            board.play(coord)

    e = process_time()

    print(board)
    print(f'{board.game_state} won with score {board.custom_player_discs_len(board.game_state)}')

    loser = player1.field if board.game_state != player1.field else player2.field

    print(f'{loser} lost with score {board.custom_player_discs_len(loser)}')

    print(f'{e - s}s duration')

minimaxi()
minimaxi_alpha_beta()