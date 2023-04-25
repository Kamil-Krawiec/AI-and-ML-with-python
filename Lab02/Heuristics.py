import random

from Lab02 import Reversi


def heuristic1(board: Reversi, player):
    return board.custom_player_discs_len(player)

def heuristic2(game: Reversi, player):
    board = game.board.items()
    board = list(board)
    my_color = player
    opp_color = game.get_oponent_field(my_color)

    V = [
        [20, -3, 11, 8, 8, 11, -3, 20],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [20, -3, 11, 8, 8, 11, -3, 20]
    ]

    my_tiles = 0
    opp_tiles = 0
    my_front_tiles = 0
    opp_front_tiles = 0

    d = 0
    p = 0

    X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
    Y1 = [0, 1, 1, 1, 0, -1, -1, -1]

    # =============================================================================================
    # 1- Piece difference, frontier disks and disk squares
    # =============================================================================================
    for i in range(8):
        for j in range(8):

            if board[i + j][1] == my_color:
                d += V[i][j]
                my_tiles += 1
            elif board[i + j][1] == opp_color:
                d -= V[i][j]
                opp_tiles += 1

            # calculates the number of blank spaces around me
            # if the tile is not empty take a step in each direction
            if board[i + j][1] != '0':
                for k in range(8):
                    x = i + X1[k]
                    y = j + Y1[k]
                    if (0 <= x < 8 and 0 <= y < 8 and
                            board[i + j][1] == '0'):
                        if board[i + j][1] == my_color:
                            my_front_tiles += 1
                        else:
                            opp_front_tiles += 1
                        break

        # =============================================================================================
        # 2 - calculates the difference between current colored tiles
        # =============================================================================================
        if my_tiles > opp_tiles:
            p = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)

    return 10 * d + p * 10


def heuristic3(game: Reversi, player):
    board = game.board.items()
    board = list(board)
    my_color = player
    opp_color = game.get_oponent_field(my_color)

    V = [
        [20, -3, 11, 8, 8, 11, -3, 20],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [20, -3, 11, 8, 8, 11, -3, 20]
    ]

    my_tiles = 0
    opp_tiles = 0
    my_front_tiles = 0
    opp_front_tiles = 0

    p = 0
    c = 0
    l = 0
    m = 0
    f = 0
    d = 0

    X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
    Y1 = [0, 1, 1, 1, 0, -1, -1, -1]

    # =============================================================================================
    # 1- Piece difference, frontier disks and disk squares
    # =============================================================================================
    for i in range(8):
        for j in range(8):

            if board[i + j][1] == my_color:
                d += V[i][j]
                my_tiles += 1
            elif board[i + j][1] == opp_color:
                d -= V[i][j]
                opp_tiles += 1

            # calculates the number of blank spaces around me
            # if the tile is not empty take a step in each direction
            if board[i + j][1] != '0':
                for k in range(8):
                    x = i + X1[k]
                    y = j + Y1[k]
                    if (0 <= x < 8 and 0 <= y < 8 and
                            board[i + j][1] == '0'):
                        if board[i + j][1] == my_color:
                            my_front_tiles += 1
                        else:
                            opp_front_tiles += 1
                        break

        # =============================================================================================
        # 2 - calculates the difference between current colored tiles
        # =============================================================================================
        if my_tiles > opp_tiles:
            p = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)

        # =============================================================================================
        # 3- calculates the blank Spaces around my tiles
        # =============================================================================================
        if my_front_tiles > opp_front_tiles:
            f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles)
        elif my_front_tiles < opp_front_tiles:
            f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles)

        # ===============================================================================================
        # 4 - Corner occupancy
        '''
        Examine all 4 corners :
        if they were my color add a point to me 
        if they were enemies add a point to the enemy
        '''
        # ===============================================================================================
        my_tiles = opp_tiles = 0
        if board[0][1] == my_color:
            my_tiles += 1
        elif board[0][1] == opp_color:
            opp_tiles += 1

        if board[7][1] == my_color:
            my_tiles += 1
        elif board[7][1] == opp_color:
            opp_tiles += 1

        if board[56][1] == my_color:
            my_tiles += 1
        elif board[56][1] == opp_color:
            opp_tiles += 1

        if board[63][1] == my_color:
            my_tiles += 1
        elif board[63][1] == opp_color:
            opp_tiles += 1

        c = 25 * (my_tiles - opp_tiles)

        # ===============================================================================================
        # 5 - Mobility
        # ===============================================================================================
        '''
        It attempts to capture the relative difference between 
        the number of possible moves for the max and the min players,
        with the intent of restricting the
        opponent’s mobility and increasing one’s own mobility
        '''
        # basically it calculates the difference between available moves
        my_tiles = len(game.custom_player_available_moves(my_color))
        opp_tiles = len(game.custom_player_available_moves(opp_color))

        if my_tiles > opp_tiles:
            m = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            m = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)

    return (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)

def heuristic4(game: Reversi, player):
    player_moves = len(game.custom_player_available_moves(player))
    opponent_moves = len(game.custom_player_available_moves(game.get_oponent_field(player)))
    return player_moves - opponent_moves
def heuristic5(game: Reversi, player):
    return random.randint(-100,100)
