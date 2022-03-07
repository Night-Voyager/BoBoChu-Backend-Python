class Room:
    def __init__(self, number=0):
        self.number = number
        self.players = []

    @property
    def number_of_players(self):
        return len(self.players)

    @property
    def websockets_of_all_players(self):
        websockets = []
        for player in self.players:
            websockets.append(player.websocket)
        return websockets


class Player:
    def __init__(self, websocket=None):
        self.websocket = websocket
        self.state = None
