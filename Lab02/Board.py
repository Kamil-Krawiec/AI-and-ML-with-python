from collections import OrderedDict

from Lab02.Coord import Coord
from Lab02.Errors import GameHasEndedError, InvalidMoveError
from Lab02.Player import Player


class Reversi:
    BLACK = '1'
    WHITE = '2'
    EMPTY = '0'

    # surrounding of a stone
    DIRECTIONS = [Coord(x, y) for x, y in [(-1, -1), (-1, 0), (0, -1), (1, -1),
                                           (-1, 1), (0, 1), (1, 0), (1, 1)]]

    GAME_STATES = {
        "IN_PROGRESS": 'In progress',
        "BLACK_WINS": 'Black wins',
        "WHITE_WINS": 'White wins',
        "TIE": 'Tie'
    }

    def __init__(self, single_player=False):
        self.black_player = Player(self.BLACK)
        self.white_player = Player(self.WHITE)

        # creating the board as 64 tiles
        self.board = OrderedDict((Coord(i, j), self.EMPTY) for i in range(8) for j in range(8))

        # placing the initial stones
        self.board[Coord(3, 3)] = self.white_player.field
        self.board[Coord(4, 4)] = self.white_player.field
        self.board[Coord(3, 4)] = self.black_player.field
        self.board[Coord(4, 3)] = self.black_player.field

        # player is the current player
        self.player = self.black_player

        # creating initial scores
        self.black_player.result, self.white_player.result = 2, 2
        self.game_state = self.GAME_STATES['IN_PROGRESS']

    # determines if the disk in the given coordination is current players or not
    def is_enemy_disc(self, coord):
        return (coord.is_in_board() and
                self.board[coord] not in [self.player.field, self.EMPTY])

    def is_ally_disc(self, coord):
        return coord.is_in_board() and self.board[coord] == self.player.field

    # checking if the disc is empty
    def is_empty_disc(self, coord):
        return coord.is_in_board() and self.board[coord] == self.EMPTY

    # returns an array of all current player discs
    def current_player_discs(self, player):
        all_coords = [Coord(i, j) for i in range(8) for j in range(8)]
        return [coord for coord in all_coords
                if self.board[coord] == player]

    # changes the turn
    def change_current_player(self):
        if self.player == self.black_player:
            self.player = self.white_player
        else:
            self.player = self.black_player

    # array of clickable coordination
    def available_fields(self):
        discs = self.current_player_discs(self.player.field)
        result = []
        for disc in discs:

            for d in self.DIRECTIONS:
                coord = disc + d
                while self.is_enemy_disc(coord):
                    coord += d
                    if self.is_empty_disc(coord):
                        result += [coord]

        return result

    # if coordination is in available filed
    def is_valid_move(self, coord):
        return coord in self.available_fields()

    def play(self, coord):
        if self.game_state != self.GAME_STATES['IN_PROGRESS']:
            raise GameHasEndedError('Game has already ended')
        if not self.is_valid_move(coord):
            raise InvalidMoveError("Not valid move")

        # fields that are flipped after a move
        won_fields = []
        for d in self.DIRECTIONS:
            current_coord = coord + d
            while self.is_enemy_disc(current_coord):
                current_coord += d

            if self.is_ally_disc(current_coord):
                won_fields += coord.to(current_coord, d)

        # change the field to the player's field
        for coord in won_fields:
            self.board[coord] = self.player.field

        # update player result after each move
        self.black_player.result = len(self.current_player_discs(1))
        self.white_player.result = len(self.current_player_discs(2))

        self.change_current_player()
        self.game_state = self.outcome()


    # run after every move
    def outcome(self):
        # change player if there is no move for first player
        if not self.available_fields():
            self.change_current_player()

            # if second player had no move determine the winner
            if not self.available_fields():
                if self.white_player.result > self.black_player.result:
                    return self.GAME_STATES["WHITE_WINS"]
                elif self.white_player.result < self.black_player.result:
                    return self.GAME_STATES["BLACK_WINS"]
                else:
                    return self.GAME_STATES["TIE"]

        return self.GAME_STATES["IN_PROGRESS"]

    def __str__(self):
        bufor = ''
        row = 0
        for i, (key, value) in enumerate(self.board.items()):

            if i % 8 == 0:
                bufor += '\n'
                bufor += str(row) + ' - '
                row += 1

            bufor += value + ' | '

        bufor += '\n' + '-' * 35
        bufor += '\n    ' + ''.join([str(i) + ' | ' for i in range(8)])
        return bufor
