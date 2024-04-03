
class Player:
    VERSION = "Chubby Alpha Unicorn"

    def check_cards(self):
        ...

    def bet(self):
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

    def betRequest(self, game_state):
        # self.game_state should be immutable - don't change it
        self.game_state = game_state

        other_players = self.get_other_active_players()

        if len(other_players) > 0 and game_state["pot"] < 2:
            return game_state["current_buy_in"] + 1

        # check_cards()

        #bet()

        return game_state["current_buy_in"] + 1

    def showdown(self, game_state):
        pass
