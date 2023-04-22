from collections import OrderedDict

'''
OrderedDict is a dictionary subclass in Python that remembers the order in which items were added. 
In a regular Python dictionary, the order of the items is not guaranteed, and it may change between 
different runs of the program or different versions of Python.
'''


# Game logic built with a huge inspiration from: https://github.com/sadeqsheikhi/reversi_python_ai

class GameHasEndedError(Exception):
    pass


class InvalidMoveError(Exception):
    pass


class InvalidCoordRangeStepError(Exception):
    pass



