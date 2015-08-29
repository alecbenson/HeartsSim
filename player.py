class Player:
    '''A class that represents a card player'''
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards
        self.score = 0

    def __str__(self):
        return self.name

    def numCards(self):
        '''Returns the number of cards in the player's hand'''
        return len(self.cards)

    def addPoints(self, points):
        '''Adds X points to the player's score'''
        self.score += points
