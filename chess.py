def populate(board: dict):
    for i in range(8):
        position1 = [i, 1]
        board[str(position1)] = Pawn(position1, False, board)
        position2 = [i, 7]
        board[str(position2)] = Pawn(position2, True, board)


def getpos(board: dict, position: list):
    return board.get(str(position), None)


class Figure:
    def __init__(self, pos: list, white: bool, board: dict):
        self.movement = None
        self.position = pos
        self.range = None
        self.white = white
        self.board = board
        self.mv = 0

    def vectormove(self, position: list, vector: list):
        if vector[0] > 0:
            position[0] += 1
            vector[0] -= 1
        elif vector[0] < 0:
            position[0] -= 1
            vector[0] += 1
        if vector[1] > 0:
            position[1] += 1
            vector[1] -= 1
        elif vector[1] < 0:
            position[1] -= 1
            vector[1] += 1

        return getpos(self.board, position)

    def move(self, directions: list):
        if directions[0] not in range(0, 8) or directions[1] not in range(0, 8):
            return [0]
        elif directions == self.position:
            return [1]
        else:
            vector = [directions[0] - self.position[0], directions[1] - self.position[1]]
            position = self.position[:]
            if (vector[0] > self.range) or (vector[1] > self.range):
                return [2]

            if (vector[0] == vector[1]) and ('x' in self.movement):
                while (vector[0] or vector[1]) not in range(-1, 2):
                    if self.vectormove(position, vector) is not None:
                        return [3]

            elif ('+' in self.movement) and (vector[0] == 0 or vector[1] == 0):
                while (vector[0] or vector[1]) not in range(-1, 2):
                    if self.vectormove(position, vector) is not None:
                        return [3]

            else:
                return [4]

            self.vectormove(position, vector)
            field = getpos(self.board, position)
            if field is not None:
                self.position = position
                self.mv += 1
                return [5, field]
            else:
                self.position = position
                self.mv += 1
                return [6]


class Pawn(Figure):
    def __init__(self, pos: list, white: bool, board: dict):
        super(Pawn, self).__init__(pos, white, board)
        self.movement = ['+']

    def move(self, directions: list):
        if self.mv == 0:
            self.range = 2
        else:
            self.range = 1

        return super(Pawn, self).move(directions)


class Bishop(Figure):
    def __init__(self, pos: list, white: bool, board: dict):
        super(Bishop, self).__init__(pos, white, board)

    def move(self, directions: list):
        super(Bishop, self).move(directions)


class Match:
    def __init__(self):
        self.board = {}

    def start(self):
        populate(self.board)
