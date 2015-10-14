# -*- coding: utf-8 -*-
import random
import card
import operator


class AI:

    def __init__(self, complexity):
        self.complexity = complexity

    def suggest_move(self, round, trick, player):
        if self.complexity == 0:
            return self._suggest_0(round, trick, player)
        elif self.complexity == 1:
            return self._suggest_1(round, trick, player)
        elif self.complexity == 2:
            return self._suggest_2(round, trick, player)
        else:
            print "Invalid complexity provided"

    def _suggest_0(self, round, trick, player):
        return player.hand.getRandomCard()

    def _suggest_1(self, round, trick, player):
        choices = {}
        for choice in player.hand:
            val = self._heuristic(round, trick, player, choice)
            choices[val] = choice

        best = min(choices.keys(), key=float)
        return choices[best]

    def _heuristic(self, round, trick, player, card_choice):
        if not trick.isLegalMove(player, card_choice):
            return 100.0

        current_trick_value = trick.value()
        chance_to_win = self.chance_of_winning(round, trick, card_choice)
        return chance_to_win

    def cards_that_can_beat(self, round, card_choice):
        count = 0
        for card in round.cards_in_play:
            if card.suit == card_choice.suit:
                if card.getWeight() > card_choice.getWeight():
                    count += 1
        return count

    def chance_of_winning(self, round, trick, card_choice):
        ''' Returns the number of cards in play that could win the trick '''
        winning_cards = 0
        current_winning_card = trick.current_winning_card()

        if current_winning_card == None:
            # Find number of cards that can beat this card
            winning_cards = self.cards_that_can_beat(round, card_choice)
        elif current_winning_card.suit == card_choice.suit:
            # If their card is higher than mine, I can't win the trick.
            if card_choice.getWeight() < current_winning_card.getWeight():
                return 0.0
            else:
                winning_cards = self.cards_that_can_beat(round, card_choice)
        else:
            # My card is not the same suit as the winning card
            return 0

        moves_left = trick.moves_left()
        num_suit_left = round.cards_of_suit_left(card_choice.suit)
        lose_chance = float(winning_cards) / num_suit_left
        result = (1 - lose_chance) ** moves_left
        return result
