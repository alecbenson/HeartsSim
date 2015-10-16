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
            return self._suggest_move_0(round, trick, player)
        elif self.complexity == 1:
            return self._suggest_move_1(round, trick, player)
        else:
            print "Invalid complexity provided"

    def suggest_pass(self, player):
        if self.complexity == 0:
            return self._suggest_pass_0(player)
        elif self.complexity == 1:
            return self._suggest_pass_1(player)
        else:
            print "Invalid complexity provided"

    def _suggest_pass_0(self, player):
        return random.choice(player.hand)

    def _suggest_pass_1(self, player):
        passes_left = len(player.hand) - 10
        suitOrder = {"♣": 1, "♦": 7, "♥": 13, "♠": 16}

        # Increase the passing priority of a suit if it can be drained easily
        for k, v in suitOrder.iteritems():
            count = player.hand.suitCount(k)
            if count <= 3:
                suitOrder[k] += (4 * passes_left * (3 - count))

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
        d_threat = self.drained_threat(round, trick, player, card_choice)

        threat = (((1 * p_heart) + (13 * p_queen) + d_threat) * moves_after) * win_chance
        return threat

    def drained_threat(self, round, trick, player, card_choice):
        drained_threat = 0
        current_position = trick.players.index(player) + 1
        next_players = trick.players[current_position:]

        for opponent in next_players:
            if opponent in player.drained_players:
                for drained_suit in player.drained_players[opponent]:
                    if drained_suit == card_choice.suit:
                        if player.debug:
                            print "{0} is drained of {1} so playing {2} of {3} might not be good" \
                                .format(opponent.name, drained_suit, card_choice.value, card_choice.suit)
                        drained_threat += 1.0/len(next_players)
        return drained_threat

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

    def _suggest_move_0(self, round, trick, player):
        return player.hand.getRandomCard()

    def _suggest_move_1(self, round, trick, player):
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
            if player.debug:
                print "PLAYING {0} of {1} : maximizing heuristic, avg: {2}" \
                    .format(max_choice.value, max_choice.suit, avg_win_chance)
            return max_choice
        else:
            if player.debug:
                print "PLAYING {0} of {1} : minimizing heuristic, avg: {2}" \
                    .format(min_choice.value, min_choice.suit, avg_win_chance)
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
        if player.debug:
            print "{0} of {1} : heuristic {2}" \
                .format(card_choice.value, card_choice.suit, score)
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
