from copy import deepcopy
from time import process_time
import itertools
import pandas as pd
from Lab02.Heuristics import *
from Lab02.Reversi import *


def minimaxi_test(board, player1, player2):
    s = process_time()
    while board.game_state == 'In progress':
        if board.player == '1':
            score, coord = player1.make_best_move(deepcopy(board))
            board.play(coord)
        else:
            score, coord = player2.make_best_move(deepcopy(board))
            board.play(coord)
    e = process_time()

    loser = player1.field if board.game_state != player1.field else player2.field

    return board.game_state, \
        board.custom_player_discs_len(board.game_state), \
        board.custom_player_discs_len(loser), \
        e - s, \
        False


def minimaxi_alpha_beta_test(board, player1, player2):
    s = process_time()
    while board.game_state == 'In progress':
        if board.player == '1':
            score, coord = player1.make_best_move_alpha_beta(deepcopy(board))
            board.play(coord)
            # print(f'player 1 coord{coord.__str__()}')
        else:
            score, coord = player2.make_best_move_alpha_beta(deepcopy(board))
            board.play(coord)

    e = process_time()


    loser = player1.field if board.game_state != player1.field else player2.field

    return board.game_state, \
        board.custom_player_discs_len(board.game_state), \
        board.custom_player_discs_len(loser), \
        e - s, \
        True

def get_all_combinations(lst):
    return list(itertools.product(lst, repeat=2))


heuristics_list = [heuristic1, heuristic2, heuristic3, heuristic4,heuristic5]

results = pd.DataFrame(columns=['game_result',
                                'winner_score',
                                'loser_score',
                                'eval_time',
                                'heuristic_p1',
                                'heuristic_p2',
                                'minimax_depth_p1',
                                'minimax_depth_p2',
                                'alpha_beta'])

for p1,p2 in get_all_combinations([2,3,1]):
    black_starts = False

    max_depth_p1 = p1
    max_depth_p2 = p2

    for h1,h2 in get_all_combinations(heuristics_list):
        player1 = Player.Player('1', heuristic=h1, maxDepth=max_depth_p1)
        player2 = Player.Player('2', heuristic=h2, maxDepth=max_depth_p2)

        board = Reversi(black=player1, white=player2, start_from_round=4, black_starts=black_starts)

        game_state_ab, win_score_ab, loss_score_ab, time_ab, alpha_beta_ab = minimaxi_alpha_beta_test(deepcopy(board),
                                                                                                      deepcopy(player1),
                                                                                                      deepcopy(player2))

        results.loc[len(results)] = [game_state_ab, win_score_ab, loss_score_ab, time_ab, h1.__name__[-1],h2.__name__[-1], max_depth_p1, max_depth_p2, alpha_beta_ab]


print(results.to_string())
print(results.groupby(['game_result','heuristic_p1','heuristic_p2']).mean()['eval_time'])

print(results.groupby(['game_result','heuristic_p1','heuristic_p2']).mean()['winner_score'])

# print(results.groupby(by=['heuristic_p1','heuristic_p2','minimax_depth_p1','minimax_depth_p2']).mean()['eval_time'])

