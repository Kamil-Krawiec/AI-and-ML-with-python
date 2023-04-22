from Lab02.Minimaxi import minimax


class Player:

    def __init__(self, field,maxDepth=2):
        # type of stones [1, 2] black or white
        self.field = field

        # minimaxi max depth
        self.maxDepth = maxDepth

    def make_best_move(self,board,enemy):
        return minimax(board,0,None,True,self.maxDepth,self.field,enemy)