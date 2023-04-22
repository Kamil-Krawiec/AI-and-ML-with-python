from Errors import *
from Lab02.Board import Reversi
from Lab02.Coord import Coord

board = Reversi()


while True:
    print(board)
    print(f"{'black' if board.player.field == '1' else 'white'} available moves")
    for coord in board.available_fields():
        print(coord)

    x,y = input("x,y coord: ").split(",")

    board.play(Coord(int(x),int(y)))



