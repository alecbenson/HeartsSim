# -*- coding: utf-8 -*-
import random
import card
import operator


class AI:

    def __init__(self, complexity):
        self.complexity = complexity

    def suggest_move(self, round, trick, player):
        ''' A dispatcher function that will play the AI at the appropriate level '''
        if self.complexity == 0:
            return self._suggest_0(round, trick, player)
        elif self.complexity == 1:
            return self._suggest_1(round, trick, player)
        elif self.complexity == 2:
            return self._suggest_2(round, trick, player)
        else:
            print "Invalid complexity provided"

    def suggest_pass(self, player):
        suitOrder = {"♣": 0, "♦": 6, "♥": 12, "♠": 15}
        choices = {}
        for card in player.hand:
            value = suitOrder.get(card.suit) + card.getWeight()
            choices[card] = value

        return max(choices, key=choices.get)

    def threat(self, round, trick, player, card_choice):
        # Probability that a point card will be played
        other_cards = float(len(round.cards_in_play) - len(player.hand))
        if other_cards == 0:
            return 0

        queen_remaining = self.queen_remaining(round, player)
        hearts_remaining = self.suit_remaining(round, player, '♥')
        p_queen = queen_remaining / other_cards
        p_heart = hearts_remaining / other_cards
        moves_after = trick.moves_left() - 1
        win_chance = self.chance_of_winning(round, trick, player, card_choice)

        threat = (((1 * p_heart) + (13 * p_queen)) * moves_after) * win_chance
        return threat

    def queen_remaining(self, round, player):
        ''' Returns true if the queen of spades is in play and the player does not have it '''
        queen_spades = card.Card('♠', 'Q')
        if queen_spades in player.hand:
            return False
        else:
            return (queen_spades in round.cards_in_play)

    def suit_remaining(self, round, player, suit):
        ''' Retrieves the number of point cards that could be played by other players '''
        count = 0
        for card in round.cards_in_play:
            count += bool(card.suit == suit)
        for card in player.hand:
            count -= bool(card.suit == suit)
        return count

    def _suggest_0(self, round, trick, player):
        return player.hand.getRandomCard()

    def _suggest_1(self, round, trick, player):
        choices = {}
        for choice in player.hand:
            val = self._heuristic(round, trick, player, choice)
            # Don't consider illegal moves
            if val == None:
                continue
            choices[choice] = val

        max_choice = self.max_heuristic(choices)
        min_choice = self.min_heuristic(choices)
        max_win_chance = self.chance_of_winning(
            round, trick, player, max_choice)
        min_win_chance = self.chance_of_winning(
            round, trick, player, min_choice)
        avg_win_chance = (max_win_chance + min_win_chance) / 2.0

        if avg_win_chance <= 0.1:
            return max_choice
        else:
            return min_choice

    def max_heuristic(self, choices):
        temp = max(choices.iteritems(), key=operator.itemgetter(1))
        choices = [k for k, v in choices.items() if v == temp[1]
                   and k.getWeight() >= temp[0].getWeight()]
        best = max(choices, key=lambda p: p.getWeight)
        return best

    def min_heuristic(self, choices):
        temp = min(choices.iteritems(), key=operator.itemgetter(1))
        choices = [k for k, v in choices.items() if v == temp[1]
                   and k.getWeight() >= temp[0].getWeight()]
        best = max(choices, key=lambda p: p.getWeight)
        return best

    def _heuristic(self, round, trick, player, card_choice):
        ''' Used by bots to decide which card to play (card with min(heuristic) ) '''
        if not trick.isLegalMove(player, card_choice):
            return None

        current_trick_value = (trick.value() / 26.0)
        current_card_value = (card_choice._getPoints() / 13.0)
        threat = self.threat(round, trick, player, card_choice)

        score = (current_card_value + current_trick_value + threat)
        return score

    def cards_that_can_beat(self, round, player, card_choice):
        ''' Returns the number of cards that are still in play that can beat card_choice in a trick '''
        count = 0
        for card in round.cards_in_play:
            if card.suit == card_choice.suit:
                if card.getWeight() > card_choice.getWeight():
                    count += 1
        for card in player.hand:
            if card.suit == card_choice.suit:
                if card.getWeight() > card_choice.getWeight():
                    count -= 1
        return count

    def chance_of_winning(self, round, trick, player, card_choice):
        ''' Returns the probability of winning the trick after playing card_choice '''
        winning_cards = 0
        current_winning_card = trick.current_winning_card()

        if current_winning_card == None:
            # Find number of cards that can beat this card
            winning_cards = self.cards_that_can_beat(
                round, player, card_choice)
        elif current_winning_card.suit == card_choice.suit:
            # If their card is higher than mine, I can't win the trick.
            if card_choice.getWeight() < current_winning_card.getWeight():
                return 0.0
            else:
                winning_cards = self.cards_that_can_beat(
                    round, player, card_choice)
        else:
            # My card is not the same suit as the winning card
            return 0

        moves_after = trick.moves_left() - 1
        num_suit_left = self.suit_remaining(round, player, card_choice.suit)
        if num_suit_left == 0:
            return 1.0
        lose_chance = float(winning_cards) / num_suit_left
        result = (1 - lose_chance) ** moves_after
        return result
