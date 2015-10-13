# -*- coding: utf-8 -*-
import hand
from random import randint


class Player:
    '''A class that represents a card player'''

    def __init__(self, name, isHuman):
        self.name = name
        self.hand = hand.Hand()
        self.score = 0
        self.passedCards = []
        self.isHuman = isHuman

    def __str__(self):
        return self.name

    def numCards(self):
        '''Returns the number of cards in the player's hand'''
        return len(self.cards)

    def addPoints(self, points):
        '''Adds X points to the player's score'''
        self.score += points

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

    def queryCardToPlay(self, prompt, round, firstCard):
        cardIndex = self._queryForCard(prompt)
        chosenCard = self.hand[cardIndex]

        if not self.hand.isLegal(chosenCard, round, firstCard):
            print "{0} MADE AN ILLEGAL MOVE!!!!\n SUPER ILLEGAL!!! SO ILLEGAL".format(self.name)
            return self.queryCardToPlay("That's not a legal move. Try again: ", round, firstCard)

        # Break hearts if the heart is a legal move and hearts is not broken
        if chosenCard.suit == "♥" and round.heartsBroken == False:
            round.breakHearts()

        self.hand.sortCards()
        return self.hand.playCard(cardIndex)

    def _queryForCard(self, prompt):
        '''
        Asks the player to select a card to remove from their hand.
        The prompt parameter is used to specify a message to display to the user.
        Returns the card object that was selected
        '''
        if self.isHuman:
            try:
                cardToPlay = raw_input("{0}, {1}".format(self.name, prompt))
                cardIndex = int(cardToPlay) - 1
                # If out of bounds, ask again
                if not self._isSelectionInBounds(cardIndex):
                    return self._queryForCard("that wasn't a valid choice. Try again: ")
                return cardIndex
            except ValueError as err:
                return self._queryForCard("that's not even a number. Try again: ")
        else:
            # TODO: break this out into its own method
            return randint(0, len(self.hand) - 1)
