from PIL import Image

directory = 'res/chess'
dictx = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7
}
dicty = {
    '8': 0,
    '7': 1,
    '6': 2,
    '5': 3,
    '4': 4,
    '3': 5,
    '2': 6,
    '1': 7
}


def populate(board: dict):
    white = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    black = [Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook]
    for i in range(8):
        position1 = [i, 1]
        board[str(position1)] = Pawn(position1, False, board)
        position2 = [i, 6]
        board[str(position2)] = Pawn(position2, True, board)
        position3 = [i, 0]
        board[str(position3)] = black[i](position3, False, board)
        position4 = [i, 7]
        board[str(position4)] = white[i](position4, True, board)


def render(board):
    base = Image.open(directory + '/frame.png')
    boardimg = Image.open(directory + '/board.png')

    for figure in board.values():
        if isinstance(figure, Figure):
            pos1, pos2 = figure.position[0] * 128, figure.position[1] * 128
            box = [pos1, pos2, pos1 + 128, pos2 + 128]
            boardimg.paste(figure.icon, box, figure.icon)

    base.paste(boardimg, (64, 64))
    path = 'res/chess/render.png'
    base.save(path)
    return path


def getpos(board: dict, position: list):
    return board.get(str(position), None)


class Figure:
    def __init__(self, pos: list, white: bool, board: dict, name: str, rang: int, mov: list):
        self.movement = mov
        self.position = pos
        self.range: int = rang
        self.white = white
        self.board = board
        self.mv = 0

        if white:
            color = '/white'
        else:
            color = '/black'
        self.icon = Image.open(directory + '/pieces' + color + '/' + name + '.png').convert('RGBA')

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
                print(directions)
                print(vector)
                return [2]

            if (vector[0] == vector[1]) and ('x' in self.movement):
                while (vector[0] or vector[1]) not in range(-1, 2):
                    if self.vectormove(position, vector) is not None:
                        return [3]

            elif ('+' in self.movement) and (vector[0] == 0 or vector[1] == 0):
                while (vector[0] or vector[1]) not in range(-1, 2):
                    if self.vectormove(position, vector) is not None:
                        return [3]

            elif ('k' in self.movement) and \
                    (vector[0] ^ vector[1] in range(-1, 2) and vector[0] ^ vector[1] in range(-2, 3)):
                self.vectormove(position, vector)

            else:
                return [4]

            self.vectormove(position, vector)
            self.board[str(self.position)] = None
            self.position = position
            self.board[str(self.position)] = self
            self.mv += 1
            field = getpos(self.board, position)

            if field is not None:
                return [5, field]
            else:
                return [6]


class Pawn(Figure):
    def __init__(self, pos: list, white: bool, board: dict):
        super(Pawn, self).__init__(pos, white, board, 'pawn', 1, ['+'])

    def move(self, directions: list):
        if self.mv == 0:
            self.range = 2
        else:
            self.range = 1

        return super(Pawn, self).move(directions)


class Bishop(Figure):
    def __init__(self, pos: list, white: bool, board: dict):
        super(Bishop, self).__init__(pos, white, board, 'bishop', 10, ['x'])


class Knight(Figure):
    def __init__(self, pos: list, white: bool, board: dict):
        super(Knight, self).__init__(pos, white, board, 'knight', 10, ['k'])


class Rook(Figure):
    def __init__(self, pos: list, white: bool, board: dict):
        super(Rook, self).__init__(pos, white, board, 'rook', 10, ['+'])


class Queen(Figure):
    def __init__(self, pos: list, white: bool, board: dict):
        super(Queen, self).__init__(pos, white, board, 'queen', 10, ['x', '+'])


class King(Figure):
    def __init__(self, pos: list, white: bool, board: dict):
        super(King, self).__init__(pos, white, board, 'king', 1, ['x', '+'])

    def move(self, directions: list):
        return super(King, self).move(directions)


class Match:
    def __init__(self):
        self.board = {}

    def start(self):
        populate(self.board)

    def image(self):
        return render(self.board)

    def move(self, arg: str, white: bool):
        movement = arg.split(':')
        start = [dictx.get(movement[0][0], 2137), dicty.get(movement[0][1], 420)]
        end = [dictx.get(movement[1][0], 69), dicty.get(movement[1][1], 100)]
        field = self.board.get(str(start))

        if not isinstance(field, Figure):
            print('huj')
            return 0
        elif field.white != white:
            print('huj1')
            return 1
        else:
            print(field.move(end))




