from Classes import *

board = Reversi()

print(board)

print("black available moves")
for coord in board.available_fields():
    print(coord)

board.change_current_player()
print("white available moves")
for coord in board.available_fields():
    print(coord)