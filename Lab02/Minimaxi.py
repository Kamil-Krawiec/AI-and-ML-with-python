from operator import itemgetter
from copy import deepcopy
from Lab02 import Reversi
from Lab02.Heuristics import heuristics1


def minimax(board: Reversi, curDepth, prev_move, maxTurn, targetDepth, me, enemy):
    # base case : targetDepth reached
    if curDepth == targetDepth:
        return heuristics1(board, me),prev_move

    if maxTurn:
        compr_list = []

        for move in board.available_moves_now:
            newBoard = deepcopy(board)
            newBoard.play(move)
            compr_list.append(
                minimax(
                    newBoard,
                    curDepth + 1,
                    move if prev_move is None else prev_move,
                    False,
                    targetDepth,
                    me,
                    enemy)
            )

        if board.round> 64-targetDepth:
            if board.game_state == enemy:
                return -float('inf'),prev_move
            elif board.game_state == me:
                return float('inf'),prev_move

        if len(compr_list)==0:
            return float('inf'),prev_move

        return max(compr_list, key=itemgetter(0))
    else:
        compr_list = []

        for move in board.available_moves_now:
            newBoard = deepcopy(board)
            newBoard.play(move)
            compr_list.append(
                minimax(
                    newBoard,
                    curDepth + 1,
                    prev_move, True, targetDepth,
                    enemy,
                    me))

        if board.round> 64-targetDepth:
            if board.game_state == enemy:
                return -float('inf'),prev_move
            elif board.game_state == me:
                return +float('inf'),prev_move

        if len(compr_list)==0:
            return -float('inf'),prev_move

        return min(compr_list, key=itemgetter(0))
