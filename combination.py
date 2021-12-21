"""
Module that containing class that represents combination of 5 cards in Texas Holdem.
"""


class Combination:
    """
    Class that represents combination of 5 cards in Texas Holdem.

    Args:
        cards (list[str]): list with cards of combinations.

    Attributes:
        self.cards (list[namedtuple[int, str]]): list with all combination cards.
        self.denominations_suits_dict (dict[int, set[str]]): dict where denominations are keys
        and their suits are in set value of this dict.
        self.denominations (set[int]): set with all denominations of combination cards.
        self.suits (set[str]): set with all suits of combination cards.
    """
    def __init__(self, cards):
        self.cards = []
        for card in cards:
            if card[:-1] == "J":
                self.cards.append((11, card[-1]))
            elif card[:-1] == "Q":
                self.cards.append((12, card[-1]))
            elif card[:-1] == "K":
                self.cards.append((13, card[-1]))
            elif card[:-1] == "A":
                self.cards.append((14, card[-1]))
            else:
                self.cards.append((int(card[:-1]), card[-1]))

        self.denominations_suits_dict = {}
        for card in self.cards:
            self.denominations_suits_dict.setdefault(card[0], set())
            self.denominations_suits_dict[card[0]].add(card[1])

        self.denominations = set(self.denominations_suits_dict)
        self.suits = set(card[-1] for card in self.cards)

    def get_combination_data(self):
        """
        Return combination data, that is needed to compare combinations
        considering Texas Holdem game rules.
        """
        if len(self.suits) == 1:

            # Checking for Royal Flush
            if self.denominations == {10, 11, 12, 13, 14}:
                return (1000,)

            # Checking for Straight Flush
            if self.denominations == set(i for i in range(min(self.denominations), min(self.denominations) + 5)):
                return (900, max(self.denominations))

            if self.denominations == {14, 2, 3, 4, 5}:
                return (900, 5)

            # Return flush
            return (600, *sorted(self.denominations_suits_dict, reverse=True))

        # Checking for Full House, Four of a Kind
        if len(self.denominations) == 2:
            for value in self.denominations_suits_dict.values():
                if len(value) != 4 and len(value) != 1:
                    for denomination, suits in self.denominations_suits_dict.items():
                        if len(suits) == 3:
                            three_denomination = denomination
                        if len(suits) == 2:
                            pair_denomination = denomination
                    return (700, three_denomination, pair_denomination)

            for denomination, suits in self.denominations_suits_dict.items():
                if len(suits) == 4:
                    four_of_a_kind = denomination
            other_cards = list(self.denominations_suits_dict)
            other_cards.remove(four_of_a_kind)
            return (800, four_of_a_kind, *sorted(other_cards, reverse=True))

        # Checkings for Straight
        if self.denominations == set(i for i in range(min(self.denominations), min(self.denominations) + 5)):
            return (500, max(self.denominations))

        if self.denominations == {2, 3, 4, 5, 14}:
            return (500, 5)

        # Checking for three of a kind, two pair
        if len(self.denominations) == 3:
            for denomination_suits in self.denominations_suits_dict.values():
                if len(denomination_suits) != 2 and len(denomination_suits) != 1:
                    for denomination, suits in self.denominations_suits_dict.items():
                        if len(suits) == 3:
                            three_denomination = denomination
                            other_cards = list(self.denominations_suits_dict)
                            other_cards.remove(three_denomination)
                            return (400, three_denomination, *sorted(other_cards, reverse=True))

            pairs_denomination = set()
            for denomination, suits in self.denominations_suits_dict.items():
                if len(suits) == 2:
                    pairs_denomination.add(denomination)
            other_cards = list(self.denominations_suits_dict)
            for denomination in set(pairs_denomination):
                other_cards.remove(denomination)
            return (300, *sorted(pairs_denomination, reverse=True), *sorted(other_cards, reverse=True))

        # Checking for One pair
        if len(self.denominations) == 4:
            for denomination, suits in self.denominations_suits_dict.items():
                if len(suits) == 2:
                    pair = denomination
            other_cards = list(self.denominations_suits_dict)
            other_cards.remove(pair)
            return (200, pair, *sorted(other_cards, reverse=True))

        return (100, *sorted(self.denominations_suits_dict, reverse=True))

    def sorted_denominations(self):
        """
        Return sorted list of all denominations of cards that are in combination.
        """
        return sorted([card[0] for card in self.cards], reverse=True)
