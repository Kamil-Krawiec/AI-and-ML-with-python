class Player:

    def __init__(self, field, AI=False):
        # type of stones [1, 2]
        self.field = field

        # score of each player
        self.result = 0
        self.AI = AI
