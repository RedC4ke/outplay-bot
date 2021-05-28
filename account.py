class Player:
    def __init__(self, user):
        self.user = user
        self.chess = ChessStats()


class ChessStats:
    def __init__(self):
        self.wins = 0
        self.loses = 0
        self.draws = 0
        self.current_game = None
