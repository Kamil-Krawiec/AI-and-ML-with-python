from copy import deepcopy
from time import process_time
import itertools
import pandas as pd
from Lab02.Heuristics import *
from Lab02.Reversi import *


def minimaxi_test(board, player1, player2):
    p1_eval_times = []
    p2_eval_times = []

    while board.game_state == 'In progress':
        if board.player == '1':
            s_1 = process_time()
            score, coord = player1.make_best_move(deepcopy(board))
            e_1 = process_time()
            p1_eval_times.append(round(e_1 - s_1, 4))
            board.play(coord)
        else:
            s_2 = process_time()
            score, coord = player2.make_best_move(deepcopy(board))
            e_2 = process_time()
            p2_eval_times.append(round(e_2 - s_2, 4))
            board.play(coord)

    loser = player1.field if board.game_state != player1.field else player2.field

    return board.game_state, \
        board.custom_player_discs_len(board.game_state), \
        board.custom_player_discs_len(loser), \
        p1_eval_times, \
        p2_eval_times, \
        False


def minimaxi_alpha_beta_test(board, player1, player2):
    p1_eval_times=[]
    p2_eval_times=[]

    while board.game_state == 'In progress':
        if board.player == '1':
            s_1 = process_time()
            score, coord = player1.make_best_move_alpha_beta(deepcopy(board))
            e_1 = process_time()
            p1_eval_times.append(round(e_1-s_1,4))
            board.play(coord)
        else:
            s_2 = process_time()

            score, coord = player2.make_best_move_alpha_beta(deepcopy(board))
            e_2 = process_time()
            p2_eval_times.append(round(e_2-s_2,4))

            board.play(coord)




    loser = player1.field if board.game_state != player1.field else player2.field

    return board.game_state, \
        board.custom_player_discs_len(board.game_state), \
        board.custom_player_discs_len(loser), \
        p1_eval_times, \
        p2_eval_times, \
        True

def get_all_combinations(lst):
    return list(itertools.product(lst, repeat=2))


heuristics_list = [heuristic1, heuristic2, heuristic3, heuristic4,heuristic5]

results = pd.DataFrame(columns=['game_id','game_result',
                                'winner_score',
                                'loser_score',
                                'heuristic_p1',
                                'heuristic_p2',
                                'minimax_depth_p1',
                                'minimax_depth_p2',
                                'p1_eval_times',
                                'p2_eval_times',
                                'alpha-beta'])
game_id=0
for p1,p2 in [(3,3),(4,4),(5,5),(6,6),(7,7)]:
    black_starts = False

    max_depth_p1 = p1
    max_depth_p2 = p2

    h1=heuristic1
    h2= heuristic3

    print(f"Heurystyka {h1},{h2}")

    player1 = Player.Player('1', heuristic=h1, maxDepth=max_depth_p1)
    player2 = Player.Player('2', heuristic=h2, maxDepth=max_depth_p2)

    board = Reversi(black=player1, white=player2, start_from_round=4, black_starts=black_starts)

    game_state_ab, win_score_ab, loss_score_ab, time_p1,time_p2, alpha_beta_ab = minimaxi_alpha_beta_test(deepcopy(board),
                                                                                                  deepcopy(player1),
                                                                                                  deepcopy(player2))

    results.loc[len(results)] = [game_id,game_state_ab, win_score_ab, loss_score_ab, h1.__name__[-1],h2.__name__[-1], max_depth_p1, max_depth_p2,time_p1,time_p2,alpha_beta_ab]
    results.at[len(results)-1,'p1_eval_times'] = time_p1
    results.at[len(results)-1,'p2_eval_times'] = time_p2
    game_id+=1

    print(f"{p1},{p2}")


results['p1_eval_times'] = results['p1_eval_times'].astype('object')
results['p2_eval_times'] = results['p2_eval_times'].astype('object')

results.to_csv('Lab02/test_alpha_beta_v2.csv')





