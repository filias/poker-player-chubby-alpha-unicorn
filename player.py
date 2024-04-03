from enum import Enum


class BetType(Enum):
    FOLD = "fold"
    CALL = "call"
    RAISE = "raise"


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

    def check_cards(self) -> BetType:
        # Very good hands
        good_hands = [
            ("A", "A"),
            ("K", "K"),
            ("Q", "Q"),
            ("J", "J"),
            ("10", "10"),
            ("9", "9"),
        ]
        if (self.first_card["rank"], self.second_card["rank"]) in good_hands:
            return BetType.RAISE

        suited_good_hands = [("A", "K"), ("K", "A"), ("A", "Q"), ("Q", "A"), ("K", "Q"), ("Q", "K")]
        if (self.first_card["rank"], self.second_card["rank"]) in suited_good_hands and self.first_card["suit"] == self.second_card["suit"]:
            return BetType.RAISE

        # Poor hands
        # Check if we have a low pair
        poor_hands = [
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
        ]
        if (self.first_card["rank"], self.second_card["rank"]) in poor_hands:
            return BetType.FOLD

        # Check if the cards are not of the same suit and not after the other
        if (self.first_card["suit"] != self.second_card["suit"]
            and not self.are_after_the_other(self.first_card["rank"], self.second_card["rank"])
            and not self.first_card["rank"] == self.second_card["rank"]):
            return BetType.FOLD

        # Middle hands
        return BetType.CALL

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
    def fold_bet(self):
        return 0
    
    def betRequest(self, game_state):
        # self.game_state should be immutable - don't change it
        self.game_state = game_state

        # If there are other playing in the game we call
        if self.other_players_count > 0:
            # If the cards are good we raise
            action = self.check_cards()
            if action == BetType.RAISE:
                return self.raise_bet
            if action == BetType.FOLD:
                return self.fold_bet
            if action == BetType.CALL:
                return self.call_bet

        # Otherwise we call as there are no other players
        return self.call_bet


    def showdown(self, game_state):
        pass
