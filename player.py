
class Player:
    VERSION = "Chubby Alpha Unicorn"

    def check_cards(self) -> bool:
        ...

    def get_other_active_players(self):
        return [
            # loop through all players
            player for player in self.game_state["players"]
            # take active players
            if player["status"] == "active"
            # don't take our own player
            and player["id"] != self.game_state["in_action"]
        ]

    @property
    def call_bet(self):
        return self.game_state["current_buy_in"] - self.game_state["players"]["in_action"]["bet"]

    @property
    def raise_bet(self):
        return self.call_bet + 1

    def betRequest(self, game_state):
        # self.game_state should be immutable - don't change it
        self.game_state = game_state

        # If there are other playing in the game we call
        other_players = self.get_other_active_players()
        if len(other_players) > 0:
            return self.call_bet

        # If the cards are good we raise
        if check_cards():
            return self.raise_bet

        # Otherwise we call
        return self.call_bet


    def showdown(self, game_state):
        pass
