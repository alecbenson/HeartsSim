# Printing cards uses use non ascii characters, we need to set encoding
# -*- coding: utf-8 -*-
from string import Template
import hearts
import sys
from functools import total_ordering


@total_ordering
class Card:
    '''A simple class that represents a standard playing card'''

    def __init__(self, suit, value, index=0):
        self.suit = suit
        self.value = value
        self.owner = ""
        self.weight = self.getWeight()
        self.loc = index
        self.template = ["${color}┌─────┐", "${color}│${spacing}${val}   │",
                         "${color}│  ${suit}  │", "${color}│   ${val}${spacing}│", "${color}└─────┘", "${color}${loc}\033[0m"]

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
        spaces = " " * (2 - len(self.value))
        if self.loc is 1:
            str_index = '{: >4}'.format(self.loc)
        else:
            str_index = '{: >7}'.format(self.loc)
        keys = dict(color=self._getColor(), val=self.value,
                    suit=self.suit, spacing=spaces, loc=str_index)

        for line in self.template:
            result.append(Template(line).substitute(keys))
        return result

    def getWeight(self):
        '''
        getWeight will determine the value of the card.
        It is used for determining which player wins the hand
        '''
        weight = 0
        try:
            return int(self.value)
        except ValueError:
            try:
                return {"J": 11, "Q": 12, "K": 13, "A": 14, }.get(self.value)
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
        if other == None:
            return False
        return self.suit == other.suit and self.value == other.value

    def __lt__(self, other):
        '''
        This function may be replaced with __le__, __gt__, or __ge__
        but one of those is required for total_ordering
        '''
        # the suitOrder dictionary is needed to ensure that cards are suited by
        # suit first, and rank second.
        suitOrder = {"♦": 100, "♣": 200, "♥": 300, "♠": 400}
        return (suitOrder.get(self.suit) + self.getWeight()) < (suitOrder.get(other.suit) + other.getWeight())
