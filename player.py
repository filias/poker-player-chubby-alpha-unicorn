
class Player:
    VERSION = "Chubby Alpha Unicorn"

    def betRequest(self, game_state):
        if game_state["bet_index"] > 2 and game_state["pot"] < 2:
            return 2
        return 1

    def showdown(self, game_state):
        pass

