class Player:
    VERSION = "Chubby Alpha Unicorn"

    @property
    def our_player_id(self):
        return self.game_state["in_action"]

    @property
    def our_player(self):
        return self.game_state["players"][self.our_player_id]

    @property
    def our_cards(self):
        return self.our_player["hole_cards"]

    @property
    def first_card(self):
        return self.our_cards[0]

    @property
    def second_card(self):
        return self.our_cards[1]

    def are_after_the_other(self, first, second) -> bool:
        to_int = {"A": 14, "K": 13, "Q": 12, "J": 11, "10": 10, "9": 9, "8": 8, "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}

        rank_1 = to_int[first]
        rank_2 = to_int[second]

        return abs(rank_1 - rank_2) == 1

    def check_cards(self) -> bool:
        very_good_hands = [
            ("A", "A"),
            ("K", "K"),
            ("Q", "Q"),
            ("J", "J"),
        ]
        return self.first_card["rank"], self.second_card["rank"]) in very_good_hands

    @property
    def other_players_count(self):
        return len([
            # loop through all players
            player for player in self.game_state["players"]
            # take active players
            if player["status"] == "active"
            # don't take our own player
            and player["id"] != self.our_player_id
        ])

    @property
    def call_bet(self):
        return max(self.game_state["current_buy_in"] - self.our_player["bet"], 0)

    @property
    def raise_bet(self):
        return self.call_bet + self.game_state["minimum_raise"]

    @property
    def raise_aggressive_bet(self):
        return self.call_bet + max(self.game_state["pot"], self.game_state["minimum_raise"])

    @property
    def fold_bet(self):
        return 0
    
    def betRequest(self, game_state):
        # self.game_state should be immutable - don't change it
        self.game_state = game_state

        # If there are other playing in the game we call
        if self.other_players_count > 0:
            if self.check_cards():
                return self.raise_aggressive_bet
            return self.fold_bet

        # Otherwise we call as there are no other players
        return self.call_bet


    def showdown(self, game_state):
        pass
