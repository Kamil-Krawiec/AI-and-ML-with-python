from copy import deepcopy

from Lab02.Player import Player
from Lab02.Reversi import *

board = Reversi()
player1 = Player('1',maxDepth=5)
player2 = Player('2')
print(board)

for x in range(60):
    if board.player == '1':
        score,coord = player1.make_best_move(deepcopy(board),'2')
        board.play(coord)
    else:
        score, coord = player2.make_best_move(deepcopy(board),'1')
        board.play(coord)

print(board)
print(f'{board.game_state} won with score {board.custom_player_discs(board.game_state)}')
print(f'{64-board.custom_player_discs(board.game_state)} score for looser')
