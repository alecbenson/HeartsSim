#Printing cards uses use non ascii characters, we need to set encoding
# -*- coding: utf-8 -*-
from random import shuffle
from string import Template
import hearts
import sys
from functools import total_ordering

@total_ordering
class Card:
    '''A simple class that represents a standard playing card'''
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.owner = ""
        self.weight = self._getWeight()
        self.template = ["${color}┌─────┐", "${color}│${spacing}${val}   │",
        "${color}│  ${suit}  │","${color}│   ${val}${spacing}│", "${color}└─────┘"]

    def __str__(self):
        '''
        This is used to display a card in string form.
        '''
        return '\n'.join(self.templatedParts())

    def _getColor(self):
        '''Gets the color that should be used for printing the card'''
        if self.suit == "♥" or self.suit == "♦":
            return "\033[31m"
        return "\033[0m"

    def templatedParts(self):
        '''
        templatedParts is a helper function that returns a list that is identical
        to self.template except that the template parameters are substituted
        '''
        result = []
        spaces = " "*(2-len(self.value))
        keys = dict(color = self._getColor(), val=self.value, suit=self.suit, spacing=spaces)

        for line in self.template:
            result.append(Template(line).substitute(keys))
        return result

    def _getWeight(self):
        '''
        getWeight will determine the value of the card.
        It is used for determining which player wins the hand
        '''
        weight = 0
        try:
            return int(self.value)
        except ValueError:
            try:
                return {"J":11, "Q":12, "K":13, "A":14,}.get(self.value)
            except KeyError as err:
                print str(err)
                sys.exit(1)

    def _getPoints(self):
        '''Returns the number of points a card is worth'''
        if(self.suit == "♥"):
            return 1
        elif(self.suit == "♠" and self.value == "Q"):
            return 13
        else:
            return 0

    def __eq__(self, other):
        '''Required for total_ordering'''
        return False

    def __lt__(self, other):
        '''
        This function may be replaced with __le__, __gt__, or __ge__
        but one of those is required for total_ordering
        '''
        #the suitOrder dictionary is needed to ensure that cards are suited by
        #suit first, and rank second.
        suitOrder = {"♦":100, "♣":200, "♥":300, "♠":400}
        return (suitOrder.get(self.suit) + self._getWeight()) < (suitOrder.get(other.suit) + other._getWeight())

class Deck:
    '''A simple class that represents a standard deck of 52 cards'''
    def __init__(self):
        self.cards = []
        self._newDeck()

    def _newDeck(self):
        '''Instantiate a new, shuffled deck'''
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["♥", "♦", "♠", "♣"]
        for value in values:
            for suit in suits:
                card = Card(suit, value)
                self.cards.append(card)
        self.shuffle()

    def __str__(self):
        return '\n'.join(str(card) for card in self.cards)

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        '''Shuffle all cards in the deck'''
        shuffle(self.cards)

    def deal(self):
        '''Pull a single card from the deck'''
        return self.cards.pop(0)

    def dealHands(self, players):
        '''Distributes the deck amongst the players'''
        while len(self.cards) != 0:
            for player in players:
                dealtCard = self.deal()
                player.hand.addCard(dealtCard)

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
            return self.cards.remove(card)
        except ValueError as err:
            print str(err)

    def sortCards(self):
        '''Sorts all of the cards in the hand'''
        self.cards.sort()

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
