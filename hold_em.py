"""
Module that containing all functions that are needed to calculate win probability of players
in Texas Holdem.
"""
import itertools as it
from math import factorial
from combination import Combination


ALL_CARDS = {
    '2S', '2C', '2D', '2H', '3S', '3C', '3D', '3H',
    '4S', '4C', '4D', '4H', '5S', '5C', '5D', '5H',
    '6S', '6C', '6D', '6H', '7S', '7C', '7D', '7H',
    '8S', '8C', '8D', '8H', '9S', '9C', '9D', '9H',
    '10S', '10C', '10D', '10H', 'JS', 'JC', 'JD', 'JH',
    'QS', 'QC', 'QD', 'QH', 'KS', 'KC', 'KD', 'KH',
    'AS', 'AC', 'AD', 'AH'
    }


def combinations_number(n, k):
    """
    Return number of combinations of k objects from a set with n object.
    """
    return factorial(n) / (factorial(n - k) * factorial(k))


def make_best_combinations(players_hands, known_community_cards):
    """
    Return the best combinations for each player hand and cards that are on the table.

    :param players_hands: players cards that are in their hands
    :type players_hands: list[tuple[str, str]]

    :param known_community_cards: cards that are in game board
    :type known_community_cards: list[str]

    :rtype best_combinations: list[tuple[tuple[int], Combination]]
    :return best_combinations: tuples where first elem is combination data to compare,
    second elem is Combination
    """
    best_combinations = [[[0]] for _ in range(len(players_hands))]
    for i, hand in enumerate(players_hands):
        for card_combination in it.combinations(hand + tuple(known_community_cards), 5):
            possible_best_combination = Combination(card_combination)
            possible_best_combination_data = possible_best_combination.get_combination_data()
            for j, best_combination_score_item in enumerate(best_combinations[i][0]):
                if best_combination_score_item > possible_best_combination_data[j]:
                    break
                if best_combination_score_item < possible_best_combination_data[j]:
                    best_combinations[i] = (possible_best_combination_data, possible_best_combination)
                    break
    return best_combinations


def count_win_five_community_cards(players_private_cards, known_community_cards):
    """
    Return list showing chance of winning for each player, knowing all five cards on table.

    :param players_private_cards: players cards that are in their hands
    :type players_private_cards: list[tuple[str, str]]

    :param known_community_cards: cards that are in game board
    :type known_community_cards: list[str]

    :rtype winners_list: list[float]
    :return winners_list: list showing who wins for certain card combination
    """
    best_players_combinations = make_best_combinations(players_private_cards, known_community_cards)
    winners_list = [0 for _ in range(len(players_private_cards))]

    winner_combination = best_players_combinations[0]
    for i, combination in enumerate(best_players_combinations[1:]):
        for j, best_combination_data_item in enumerate(combination[0]):
            if winner_combination[0][j] < best_combination_data_item:
                winner_combination = combination
            if winner_combination[0][j] > best_combination_data_item:
                break

    winner_combination_suits = winner_combination[1].sorted_denominations()
    winner_combination_type = winner_combination[0][0]

    count_winners = 0
    for comb in best_players_combinations:
        if winner_combination_suits == comb[1].sorted_denominations() and comb[0][0] == winner_combination_type:
            count_winners += 1

    for i, comb in enumerate(best_players_combinations):
        if winner_combination_suits == comb[1].sorted_denominations() and comb[0][0] == winner_combination_type:
            winners_list[i] += 1 / count_winners
    return winners_list


def count_win_probabilities(players_private_cards, known_community_cards, already_dropped_cards={}):
    """
    Count win probabilities in Texas Holdem for each player knowing their cards in hands,
    cards on the table and already dropped cards.

    :param players_private_cards: players cards that are in their hands
    :type players_private_cards: list[tuple[str, str]]

    :param known_community_cards: cards that are in game board
    :type known_community_cards: list[str]

    :param already_dropped_cards: cards that were dropped, they can't be in this and next rounds
    :type already_dropped_cards: list[str]

    :rtype win_probabilities: list[float]
    :return win_probabilities: total win probabilities for each player and
    all possible combinations of cards
    """
    if len(known_community_cards) == 5:
        return count_win_five_community_cards(players_private_cards, known_community_cards)

    possible_cards = (
        ALL_CARDS
        - set(already_dropped_cards)
        - set(known_community_cards)
        - set(card for player_hand in players_private_cards for card in player_hand)
    )
    win_probabilities = [0 for _ in range(len(players_private_cards))]

    for card_combination in it.combinations(possible_cards, 5 - len(known_community_cards)):
        win_probabilities_per_combination = count_win_five_community_cards(
            players_private_cards,
            (*known_community_cards, *card_combination)
        )
        for i, possible in enumerate(win_probabilities_per_combination):
            win_probabilities[i] += possible

    number_of_possible_combinations = combinations_number(
        len(possible_cards),
        5 - len(known_community_cards)
    )
    print(number_of_possible_combinations)

    for i in range(len(win_probabilities)):
        win_probabilities[i] /= number_of_possible_combinations
    return win_probabilities
