from Lab02.Errors import InvalidCoordRangeStepError


class Coord:
    # on definition, we pass x and y values to class
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # gets two coordination and returns the sum of them as new Coord
    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    # compares two Coords
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __hash__(self):
        return hash((self.x, self.y))

    # string representation of object
    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    # defines if Coord is in right domain
    def is_in_board(self):
        return min(self.x, self.y) >= 0 and max(self.x, self.y) < 8

    # maybe related to flipping
    def to(self, end, step):
        if (end.x - self.x) * step.y != (end.y - self.y) * step.x:
            raise InvalidCoordRangeStepError()

        result = []
        coord = self
        while coord != end:
            result.append(coord)
            coord += step
        return result

