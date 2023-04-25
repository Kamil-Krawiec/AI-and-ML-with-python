from copy import deepcopy
from Lab02.Reversi import *


class Minimaxi():
    def __init__(self, heur_func_mm):
        self.heuristic = heur_func_mm

    def minimax(self, board, curDepth, prev_move, maxTurn, targetDepth, player):

        if curDepth == targetDepth or board.game_state != 'In progress' \
                or (len(board.current_player_available_moves()) == 0 and prev_move is not None):

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

            avaible_moves = board.current_player_available_moves()
            for move in avaible_moves:
                newBoard = deepcopy(board)

                prev_move = move if curDepth == 0 else prev_move

                newBoard.play(move)

                score, cand_move = self.minimax(
                    newBoard,
                    curDepth + 1,
                    prev_move,
                    False,
                    targetDepth,
                    player
                )

                if score == float('inf'): return score, cand_move

                if score > max_score:
                    max_score = score
                    best_move = cand_move

            return max_score, prev_move if best_move is None else best_move

        else:

            min_score = float('inf')
            best_move = None
            avaible_moves = board.current_player_available_moves()

            for move in avaible_moves:
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

                if score == -float('inf'): return score, cand_move

                if score < min_score:
                    min_score = score
                    best_move = cand_move

            return min_score, prev_move if best_move is None else best_move

    def minimax_alfa_beta(self, board, curDepth, prev_move, maxTurn, targetDepth, player, alpha, beta):
        if curDepth == targetDepth or board.game_state != 'In progress' \
                or (len(board.current_player_available_moves()) == 0 and prev_move is not None):

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

            avaible_moves = board.current_player_available_moves()

            for move in avaible_moves:

                prev_move = move if curDepth == 0 else prev_move

                newBoard = deepcopy(board)

                newBoard.play(move)

                score, cand_move = self.minimax_alfa_beta(
                    newBoard,
                    curDepth + 1,
                    prev_move,
                    False,
                    targetDepth,
                    player,
                    alpha,
                    beta
                )

                if score == float('inf'): return score, cand_move

                if score > max_score:
                    max_score = score
                    best_move = cand_move

                alpha = max(alpha, score)

                if alpha >= beta:
                    break

            return max_score, prev_move if best_move is None else best_move


        else:

            min_score = float('inf')
            best_move = None
            avaible_moves = board.current_player_available_moves()

            for move in avaible_moves:
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

                if score == -float('inf'): return score, cand_move

                if score < min_score:
                    min_score = score
                    best_move = cand_move

                beta = min(beta, score)

                if alpha >= beta:
                    break

            return min_score, prev_move if best_move is None else best_move
