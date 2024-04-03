import requests


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

    def check_cards_pre_flop(self) -> bool:
        very_good_hands = [
            ("A", "A"),
            ("K", "K"),
            ("Q", "Q"),
            ("J", "J"),
        ]
        return (self.first_card["rank"], self.second_card["rank"]) in very_good_hands

    def check_cards_post_flop(self) -> bool:
        very_good_hands = [
            ("A", "A"),
            ("K", "K"),
            ("Q", "Q"),
            ("J", "J"),
        ]
        return (self.first_card["rank"], self.second_card["rank"]) in very_good_hands
        
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
        return max(self.game_state["current_buy_in"] - self.our_player["bet"], 1)

    @property
    def raise_bet(self):
        return self.call_bet + self.game_state["minimum_raise"]

    @property
    def raise_aggressive_bet(self):
        return self.call_bet + max(self.game_state["pot"], self.game_state["minimum_raise"])

    @property
    def fold_bet(self):
        return 0

    @property
    def pot_at_big_blind(self):
        return self.game_state["current_buy_in"] == 2 * self.game_state["small_blind"]

    @property
    def at_blind(self):
        return self.game_state["dealer"] in (2, 3)

    @property
    def post_flop(self):
        return self.game_state["community_cards"]

    def betRequest(self, game_state):
        # self.game_state should be immutable - don't change it
        self.game_state = game_state

        # post flop
        if self.post_flop:
            # api_url = "https://rainman.leanpoker.org/rank"
            #
            # cards = [
            #             {"rank": self.first_card["rank"], "suit": self.first_card["suit"]},
            #             {"rank": self.second_card["rank"], "suit": self.second_card["suit"]},
            #         ] + self.game_state["community_cards"]
            #
            # response = requests.get(api_url, json={"cards": cards})
            #
            # if response.json()["rank"] >= 1:
            #     return self.raise_aggressive_bet
            print("***** community cards: ", self.game_state["community_cards"])

            if self.check_cards_post_flop():
                return self.raise_aggressive_bet

            return self.fold_bet

        # pre flop
        else:

            if self.check_cards_pre_flop():
                return self.raise_aggressive_bet

            if self.at_blind and self.pot_at_big_blind:
                self.call_bet
            
            return self.fold_bet


    def showdown(self, game_state):
        pass
