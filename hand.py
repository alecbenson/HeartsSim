import card

class Hand:
    '''A class to contain the set of cards a player has available'''
    def __init__(self):
        self.cards = []

    def __len__(self):
        '''Returns the number of cards in the hand'''
        return len(self.cards)

    def addCard(self, card):
        '''Puts the given card in the player's hand'''
        self.cards.append(card)

    def empty(self):
        '''Empties the hand'''
        self.cards = []

    def playCard(self, card):
        ''' Removes the card from the player's hand and puts it in play.'''
        try:
            return self.cards.pop(card)
        except ValueError as err:
            print str(err)

    def sortCards(self):
        '''Sorts all of the cards in the hand'''
        self.cards.sort()
        for i in range(len(self.cards)):
            (self.cards[i]).loc = i + 1

    def __str__(self):
        #Please find it within yourselves to forgive me for the following
        self.sortCards()
        #Split the cards into a list of 5 elements (one for each line of the card).
        #Each element will contain a tuple consisting of
        #X elements, where X is the # of cards in the hand
        zipped = zip(*[card.templatedParts() for card in self.cards])

        #Now, we convert each element of 'zipped' into a string, and join them by newlines
        result = "\n".join("".join(map(str,l)) for l in zipped)
        return result