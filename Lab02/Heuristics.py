from Lab02 import Reversi


def heuristics1(board: Reversi,player):
    return board.custom_player_discs(player)