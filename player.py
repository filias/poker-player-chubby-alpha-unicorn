
class Player:
    VERSION = "Chubby Alpha Unicorn"

    def check_cards(self):
        ...

    def bet(self):
        ...

    def betRequest(self, game_state):
        if game_state["bet_index"] > 2 and game_state["pot"] < 2:
            return game_state["current_buy_in"] + 1

        #check_cards()

        #bet()

        return 1

    def showdown(self, game_state):
        pass

