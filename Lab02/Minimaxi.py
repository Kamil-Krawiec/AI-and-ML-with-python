from copy import deepcopy
from Lab02.Reversi import *


class Minimaxi():
    def __init__(self, heur_func_mm):
        self.heuristic = heur_func_mm

    def minimax(self, board, curDepth, prev_move, maxTurn, targetDepth, player):

        if curDepth == targetDepth or board.game_state != 'In progress' \
                or (len(board.available_moves_now) == 0 and prev_move is not None):

            if board.game_state == player:
                return float('inf'), prev_move

            elif board.game_state == 'Tie':
                return 0, prev_move

            elif board.game_state != 'In progress':
                return -float('inf'), prev_move

            return self.heuristic(board, player), prev_move

        if maxTurn:

            max_score = -float('inf')
            best_move = None

            for move in board.available_moves_now:
                newBoard = deepcopy(board)

                newBoard.play(move)

                score, cand_move = self.minimax(
                    newBoard,
                    curDepth + 1,
                    move if prev_move is None else prev_move,
                    False,
                    targetDepth,
                    player
                )

                if score >= max_score:
                    max_score = score
                    best_move = cand_move

            return max_score, best_move
        else:

            min_score = float('inf')
            best_move = None

            for move in board.available_moves_now:
                newBoard = deepcopy(board)
                newBoard.play(move)

                score, cand_move = self.minimax(
                    newBoard,
                    curDepth + 1,
                    prev_move,
                    True,
                    targetDepth,
                    player
                )

                if score <= min_score:
                    min_score = score
                    best_move = cand_move

            return min_score, best_move

    def minimax_alfa_beta(self, board, curDepth, prev_move, maxTurn, targetDepth, player, alpha, beta):
        if curDepth == targetDepth or board.game_state != 'In progress' \
                or (len(board.available_moves_now) == 0 and prev_move is not None):
            if board.game_state == player:
                return float('inf'), prev_move
            elif board.game_state == 'Tie':
                return 0, prev_move
            elif board.game_state != 'In progress':
                return -float('inf'), prev_move

            return self.heuristic(board, player), prev_move

        if maxTurn:

            max_score = -float('inf')
            best_move = None

            for move in board.available_moves_now:
                newBoard = deepcopy(board)

                newBoard.play(move)

                score, cand_move = self.minimax_alfa_beta(
                    newBoard,
                    curDepth + 1,
                    move if prev_move is None else prev_move,
                    False,
                    targetDepth,
                    player,
                    alpha,
                    beta
                )

                if score >= max_score:
                    max_score = score
                    best_move = cand_move

                alpha = max(alpha, score)

                if alpha >= beta:
                    break

            return max_score, best_move
        else:

            min_score = float('inf')
            best_move = None

            for move in board.available_moves_now:
                newBoard = deepcopy(board)
                newBoard.play(move)

                score, cand_move = self.minimax_alfa_beta(
                    newBoard,
                    curDepth + 1,
                    prev_move,
                    True,
                    targetDepth,
                    player,
                    alpha,
                    beta
                )

                if score is None: continue

                if score <= min_score:
                    min_score = score
                    best_move = cand_move

                beta = min(beta, score)
                if alpha >= beta:
                    break

            return min_score, best_move
