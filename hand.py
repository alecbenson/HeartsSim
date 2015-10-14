# -*- coding: utf-8 -*-
import card
import random


class Hand:
    '''A class to contain the set of cards a player has available'''

    def __init__(self):
        self.cards = []

    def __len__(self):
        '''Returns the number of cards in the hand'''
        return len(self.cards)

    def add_cards(self, cards):
        '''Puts the given card in the hand'''
        self.cards.extend(cards)

    def add_card(self, card):
        '''Puts the given card in the hand'''
        self.cards.append(card)

    def empty(self):
        '''Empties the hand'''
        self.cards = []

    def play_card(self, choice):
        ''' Removes the card from the hand and puts it in play.'''
        try:
            self.cards.remove(choice)
            return choice
        except TypeError as err:
            print "Invalid type provided"

    def getRandomCard(self):
        return random.choice(self)


    def __getitem__(self, index):
        return self.cards[index]

    def sortCards(self):
        '''Sorts all of the cards in the hand'''
        self.cards.sort()
        for i in range(len(self.cards)):
            (self.cards[i]).loc = i + 1

    def hasSuit(self, suit):
        for card in self.cards:
            if card.suit == suit:
                return True
        return False

    def onlyHeartsLeft(self):
        for card in self.cards:
            if card.suit != '♥':
                return False
        return True

    def __str__(self):
        # Please find it within yourselves to forgive me for the following
        self.sortCards()
        # Split the cards into a list of 5 elements (one for each line of the card).
        # Each element will contain a tuple consisting of
        # X elements, where X is the # of cards in the hand
        zipped = zip(*[card.templatedParts() for card in self.cards])

        # Now, we convert each element of 'zipped' into a string, and join them
        # by newlines
        result = "\n".join("".join(map(str, l)) for l in zipped)
        return result
