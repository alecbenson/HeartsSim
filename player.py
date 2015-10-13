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

    def queryCardToPass(self):
        return self._queryForCard("select a card that you would like to pass: ")

    def queryCardToPlay(self):
        return self._queryForCard("select a card that you would like to play: ")

    def _queryForCard(self, prompt):
        '''
        Asks the player to select a card to remove from their hand.
        The prompt parameter is used to specify a message to display to the user.
        Returns the card object that was selected
        '''
        if self.isHuman:
            cardToPlay = raw_input("{0}, {1}".format(self.name, prompt))
            try:
                cardIndex = int(cardToPlay) - 1
                if cardIndex >= len(self.hand) or cardIndex < 0:
                    raise ValueError("Out of bounds card index.")
            except ValueError as err:
                print "That's not a valid item in your hand. Try again:"
                return self.queryCardToPlay()
            return self.hand.playCard(cardIndex)
        else:
            '''
            Bots play a random card
            '''
            return self.hand.playCard(randint(0, len(self.hand) - 1))
