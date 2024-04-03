
class Player:
    VERSION = "Chubby Alpha Unicorn"

    @property
    def our_player(self):
        return self.game_state["players"][self.game_state["in_action"]]

    @property
    def our_cards(self):
        return self.our_player["hole_cards"]

    @property
    def first_card(self):
        return self.our_cards[0]

    @property
    def second_card(self):
        return self.our_cards[1]

    def check_cards(self) -> bool:
        # Check if we have a pair
        if self.our_cards[0]["rank"] == self.our_cards[1]["rank"]:
            return True

        # Check if we have a high card
        if self.first_card["rank"] in ["A", "K", "Q", "J", "10"] or self.second_card["rank"] in ["A", "K", "Q", "J", "10"]:
            return True

        return False

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
        return max(self.game_state["current_buy_in"] - self.our_player["bet"], 0)

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
        if self.check_cards():
            return self.raise_bet

        # Otherwise we call
        return self.call_bet


    def showdown(self, game_state):
        pass
