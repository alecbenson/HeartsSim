# -*- coding: utf-8 -*-
import hand
import random


class Player_Base:

    def __str__(self):
        return self.name

    def numCards(self):
        '''Returns the number of cards in the player's hand'''
        return len(self.cards)

    def addPoints(self, points):
        '''Adds X points to the player's score'''
        self.score += points


class Bot(Player_Base):

    def __init__(self, name):
        self.name = name
        self.hand = hand.Hand()
        self.score = 0
        self.passedCards = []

    def queryCardToPass(self):
        choice = random.choice(self.hand)
        return self.hand.playCard(choice)

    def queryCardToPlay(self, prompt, firstCard):
        return random.choice(self.hand)


class Human(Player_Base):
    '''A class that represents a card player'''

    def __init__(self, name):
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
        cardIndex = self._queryForCard(
            "select a card that you would like to pass: ")
        return self.hand.playCard(cardIndex)

    def queryCardToPlay(self, prompt, firstCard):
        cardIndex = self._queryForCard(prompt)
        chosenCard = self.hand[cardIndex]
        return chosenCard

    def _queryForCard(self, prompt):
        '''
        Asks the player to select a card to remove from their hand.
        The prompt parameter is used to specify a message to display to the user.
        Returns the card object that was selected
        '''
        print self.hand

        try:
            cardToPlay = raw_input("{0}, {1}".format(self.name, prompt))
            cardIndex = int(cardToPlay) - 1
        except ValueError as err:
            return self._queryForCard("that's not even a number. Try again: ")

        # If out of bounds, ask again
        if not self._isSelectionInBounds(cardIndex):
            return self._queryForCard("that wasn't a valid choice. Try again: ")
        return cardIndex
