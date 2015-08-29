#Printing cards uses use non ascii characters, we need to set encoding
# -*- coding: utf-8 -*-
from random import shuffle
from string import Template
import hearts

class Card:
    '''A simple class that represents a standard playing card'''
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.owner = ""
        self.weight = self.__getWeight()
        self.template = ["┌─────────┐", "│${val}       │",
        "│         │", "│    ${suit}    │",
        "│         │", "│       ${val}│", "└─────────┘"]

    def __str__(self):
        temp = '\n'.join(str(line) for line in self.template)
        keys = dict(val=self.value, suit=self.suit)
        formatted = Template(temp).substitute(keys)
        return formatted

    def __getWeight(self):
        '''getWeight will determine the value of the card. It is used for determining which player wins the hand'''
        try:
            return int(self.value)
        except ValueError:
            return {
            "J":11,
            "Q":12,
            "K":13,
            "A":14,
            }.get(self.value)

class Deck:
    '''A simple class that represents a standard deck of 52 cards'''
    def __init__(self):
        self.count = 52
        self.values = [" 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9", "10", " J", " Q", " K", " A"]
        self.suits = ["♥", "♦", "♠", "♣"]
        self.cards = []
        self.__newDeck()

    def __newDeck(self):
        '''Instantiate a new, shuffled deck'''
        for value in self.values:
            for suit in self.suits:
                card = Card(suit, value)
                self.cards.append(card)
        self.shuffle()

    def __str__(self):
        return '\n'.join(str(card) for card in self.cards)

    def shuffle(self):
        '''Shuffle all cards in the deck'''
        shuffle(self.cards)

    def deal(self):
        '''Deal a single card from the deck'''
        self.shuffle()
        return self.cards.pop(0)

if __name__ == '__main__':
    game = hearts.HeartsGame()
