from Lab02.Minimaxi import *


class Player:

    def __init__(self, field,maxDepth=2,heuristic=None):
        # type of stones [1, 2] black or white
        self.field = field

        # minimaxi max depth
        self.maxDepth = maxDepth

        self.minimaxi = Minimaxi(heuristic)

    def make_best_move(self,board):
        return self.minimaxi.minimax(board,0,None,True,self.maxDepth,self.field)

    def make_best_move_alpha_beta(self,board):
        return self.minimaxi.minimax_alfa_beta(board,0,None,True,self.maxDepth,self.field,-float('inf'),float('inf'))