# -*- coding: utf-8 -*-
import hand
import random
import ai


class Player_Base:

    def __str__(self):
        return self.name

    def numCards(self):
        '''Returns the number of cards in the player's hand'''
        return len(self.cards)

    def addPoints(self, points):
        '''Adds X points to the player's score'''
        self.score += points

    def forget_drained_cards(self):
        return

    def remember_drained_suit(self, opponent, card):
        return


class Bot(Player_Base):

    def __init__(self, name, complexity):
        self.name = name
        self.hand = hand.Hand()
        self.score = 0
        self.debug = False
        self.passedCards = []
        self.intelligence = ai.AI(complexity)
        self.drained_players = dict()

    def queryCardToPass(self):
        suggestion = self.intelligence.suggest_pass(self)
        if self.debug:
            print self.hand
            print "{0} passed the {1} of {2}\n\n\n" \
                .format(self.name, suggestion.value, suggestion.suit)
        return self.hand.play_card(suggestion)

    def queryCardToPlay(self, prompt, round, trick):
        if self.debug:
            print self.hand
            print "It's {0}'s turn to play: ".format(self.name)
        return self.intelligence.suggest_move(round, trick, self)

    def remember_drained_suit(self, opponent, drained_suit):
        if opponent == self:
            return
        if opponent in self.drained_players:
            if drained_suit in self.drained_players[opponent]:
                return
        self.drained_players.setdefault(opponent, []).append(drained_suit)

    def forget_drained_cards(self):
        self.drained_players = dict()


class Human(Player_Base):
    '''A class that represents a card player'''

    def __init__(self, name, complexity=0):
        self.name = name
        self.hand = hand.Hand()
        self.score = 0
        self.passedCards = []

    def _isSelectionInBounds(self, index):
        '''
        Makes sure that the index the player chose is in their hand.
        The index is the zero indexed choice of the player
        '''
        try:
            if index >= len(self.hand) or index < 0:
                raise ValueError("Out of bounds card index.")
        except ValueError as err:
            return False
        return True

    def queryCardToPass(self):
        print self.hand
        chosenCard = self._queryForCard(
            "select a card that you would like to pass: ")
        return self.hand.play_card(chosenCard)

    def queryCardToPlay(self, prompt, round, trick):
        print self.hand
        chosenCard = self._queryForCard(prompt)
        return chosenCard

    def _queryForCard(self, prompt):
        '''
        Asks the player to select a card to remove from their hand.
        The prompt parameter is used to specify a message to display to the user.
        Returns the card object that was selected
        '''
        try:
            cardToPlay = raw_input("{0}, {1}".format(self.name, prompt))
            cardIndex = int(cardToPlay) - 1
        except ValueError as err:
            return self._queryForCard("that's not even a number. Try again: ")

        # If out of bounds, ask again
        if not self._isSelectionInBounds(cardIndex):
            return self._queryForCard("that wasn't a valid choice. Try again: ")
        return self.hand[cardIndex]
