from cards import Hand

class Player:
    '''A class that represents a card player'''
    def __init__(self, name, isHuman):
        self.name = name
        self.hand = Hand()
        self.score = 0
        self.isHuman = False

    def __str__(self):
        return self.name

    def numCards(self):
        '''Returns the number of cards in the player's hand'''
        return len(self.cards)

    def addPoints(self, points):
        '''Adds X points to the player's score'''
        self.score += points
