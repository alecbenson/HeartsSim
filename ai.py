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

    def threat(self, round, player):
        #Probability that a point card will be played
        pcr = self.point_cards_remaining(round, player)
        other_cards = float(len(round.cards_in_play) - len(player.hand))

        if other_cards == 0:
            return 0

        p_point_card = pcr / other_cards

        #Is the queen still a threat?
        queen_remaining = self.queen_spades_remaining(round, player)
        hearts_remaining = round.cards_of_suit_left('♥')

        percent_points_remaining = ((13 * queen_remaining) + hearts_remaining)/16.0
        return p_point_card * percent_points_remaining

    def queen_spades_remaining(self, round, player):
        ''' Returns true if the queen of spades is in play and the player does not have it '''
        queen_spades = card.Card('♠', 'Q')
        if queen_spades in player.hand:
            return False
        else:
            return (queen_spades in round.cards_in_play)

    def point_cards_remaining(self, round, player):
        ''' Retrieves the number of point cards that could be played by other players '''
        count = 0
        for card in round.cards_in_play:
            if card._getPoints() > 0:
                count += 1
        for card in player.hand:
            if card._getPoints > 0:
                count -= 1
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
            print val

        if self.drained_of_lead(trick, player):
            return max(choices, key=choices.get)
        else:
            return min(choices, key=choices.get)


    def drained_of_lead(self, trick, player):
        winning_card = trick.current_winning_card()
        if winning_card == None:
            return False

        if not player.hand.hasSuit(winning_card.suit):
            return True
        return False


    def _heuristic(self, round, trick, player, card_choice):
        ''' Used by bots to decide which card to play (card with min(heuristic) ) '''
        if not trick.isLegalMove(player, card_choice):
            return None

        current_trick_value = trick.value()
        current_card_value = card_choice._getPoints()
        threat = self.threat(round, player)
        weight_factor = (card_choice.getWeight() / 14.0)
        chance_to_win = max(0.01, self.chance_of_winning(round, trick, card_choice))

        score = (current_card_value + current_trick_value + threat + weight_factor) * chance_to_win
        return score

    def cards_that_can_beat(self, round, card_choice):
        ''' Returns the number of cards that are still in play that can beat card_choice in a trick '''
        count = 0
        for card in round.cards_in_play:
            if card.suit == card_choice.suit:
                if card.getWeight() > card_choice.getWeight():
                    count += 1
        return count

    def chance_of_winning(self, round, trick, card_choice):
        ''' Returns the probability of winning the trick after playing card_choice '''
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
