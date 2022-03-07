class Room:
    def __init__(self, number=0):
        self.number = number
        self.players = []

    @property
    def number_of_players(self):
        return len(self.players)


class Player:
    def __init__(self):
        self.websocket = None
        self.state = None
